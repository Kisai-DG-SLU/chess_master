
import { Component, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { NgxChessBoardModule, NgxChessBoardComponent } from 'ngx-chess-board';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  standalone: true,
  imports: [CommonModule, FormsModule, NgxChessBoardModule]
})
export class AppComponent {
  @ViewChild('board', { static: false }) board!: NgxChessBoardComponent;
  playerLevel = 'intermediate';
  analysisData: any = null;
  errorMessage: string = '';
  friendlyMove: string = '';
  friendlyEval: string = '';
  videos: any[] = [];
  allRecommendations: string[] = [];
  currentOpening: string = '';
  youtubeQuota: any = null;
  youtubeFiltered: any = null;
  private apiBase = `http://${window.location.hostname}:8000`;

  // MongoDB
  username = '';
  email = '';
  userId = '';
  gameSaved = false;
  userGames: any[] = [];

  resetBoard() { if (this.board) this.board.reset(); }
  setPosition(fen: string) { if (this.board) this.board.setFEN(fen); }
  setRuyLopez() { this.setPosition('r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3'); }
  setSicilian() { this.setPosition('rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKB1R w KQkq c6 0 2'); }

  analyzePosition() {
    if (!this.board) return;
    const fen = this.board.getFEN();
    this.errorMessage = '';
    this.analysisData = null;
    this.youtubeQuota = null;
    this.youtubeFiltered = null;
    this.allRecommendations = [];

    fetch(`${this.apiBase}/analyze`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ position: fen, player_level: this.playerLevel })
    })
    .then(res => res.json())
    .then(data => {
      this.analysisData = data;
      this.friendlyMove = 'Inconnu';
      this.friendlyEval = 'Non disponible';
      this.parseStockfish(data?.analysis?.result || '');

      if (data?.recommendations?.length > 0) {
        this.allRecommendations = data.recommendations;
        const openingName = data.recommendations[0].split(' - ')[0];
        this.currentOpening = openingName;
        this.fetchVideosForAllOpenings();
      }
    })
    .catch(err => {
      this.errorMessage = 'Erreur API: ' + err.message;
    });
  }
    })
    .catch(err => {
      this.errorMessage = 'Erreur API: ' + err.message;
    });
  }

  fetchVideos(opening: string) {
    fetch(`${this.apiBase}/api/v1/videos?opening=${encodeURIComponent(opening)}`)
    .then(res => res.json())
    .then(data => {
      this.videos = data.videos || [];
      this.youtubeQuota = data.quota || null;
      this.youtubeFiltered = data.filtered || null;
    })
    .catch(err => {
      this.videos = [];
    });
  }

  fetchVideosForAllOpenings() {
    this.videos = [];
    const promises = this.allRecommendations.map(rec => {
      const opening = rec.split(' - ')[0];
      return fetch(`${this.apiBase}/api/v1/videos?opening=${encodeURIComponent(opening)}`)
        .then(res => res.json())
        .then(data => ({ opening, videos: (data.videos || []).slice(0, 2) }))
        .catch(() => ({ opening, videos: [] }));
    });
    Promise.all(promises).then(results => {
      results.forEach(r => {
        this.videos.push(...r.videos.map(v => ({ ...v, recommendation: r.opening })));
      });
    });
  }

  createUser() {
    if (!this.username || !this.email) {
      this.errorMessage = "Veuillez remplir le nom et l'email";
      return;
    }

    fetch(`${this.apiBase}/users`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username: this.username,
        email: this.email,
        level: this.playerLevel
      })
    })
    .then(res => res.json())
    .then(data => {
      this.userId = data.user_id;
      this.username = '';
      this.email = '';
      this.loadUserGames();
    })
    .catch(err => {
      this.errorMessage = 'Erreur lors de la création: ' + err.message;
    });
  }

  saveGame() {
    if (!this.userId || !this.analysisData) return;

    fetch(`${this.apiBase}/games`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        user_id: this.userId,
        position: this.board.getFEN(),
        analysis: this.analysisData,
        recommendations: this.analysisData.recommendations
      })
    })
    .then(res => res.json())
    .then(data => {
      this.gameSaved = true;
      setTimeout(() => this.gameSaved = false, 3000);
      this.loadUserGames();
    })
    .catch(err => {
      this.errorMessage = 'Erreur sauvegarde: ' + err.message;
    });
  }

  loadUserGames() {
    if (!this.userId) return;

    fetch(`${this.apiBase}/users/${this.userId}/games`)
    .then(res => res.json())
    .then(data => {
      this.userGames = data.games || [];
    })
    .catch(err => {
      this.userGames = [];
    });
  }

  parseStockfish(raw: string) {
    this.friendlyMove = 'Inconnu';
    this.friendlyEval = 'Non disponible';
    if (!raw) return;
    try {
      const moveMatch = raw.match(/Best move: ([a-h][1-8])([a-h][1-8])/);
      if (moveMatch) this.friendlyMove = `Déplacer la pièce de ${moveMatch[1]} vers ${moveMatch[2]}`;

      const cpMatch = raw.match(/'type': 'cp', 'value': (-?\d+)/);
      const mateMatch = raw.match(/'type': 'mate', 'value': (-?\d+)/);

      if (cpMatch) {
        const score = parseInt(cpMatch[1], 10) / 100;
        this.friendlyEval = score === 0 ? "Équilibré (0.00)" : (score > 0 ? `Avantage Blancs (+${score})` : `Avantage Noirs (${score})`);
      } else if (mateMatch) {
        const moves = parseInt(mateMatch[1], 10);
        this.friendlyEval = `Mat forcé en ${Math.abs(moves)} coups !`;
      }
    } catch (e) {
      this.friendlyEval = raw;
    }
  }
}
