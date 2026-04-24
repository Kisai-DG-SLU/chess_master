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
  currentOpening: string = '';
  private apiBase = `http://${window.location.hostname}:8000`;
  private apiBase = `http://${window.location.hostname}:8000`;

  resetBoard() { if (this.board) this.board.reset(); }
  setPosition(fen: string) { if (this.board) this.board.setFEN(fen); }
  setRuyLopez() { this.setPosition('r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3'); }
  setSicilian() { this.setPosition('rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKB1R w KQkq c6 0 2'); }

  analyzePosition() {
    if (!this.board) return;
    const fen = this.board.getFEN();
    this.errorMessage = '';
    this.analysisData = null;

    fetch(`${this.apiBase}/analyze`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ position: fen, player_level: this.playerLevel })
    })
    .then(res => res.json())
    .then(data => {
      this.analysisData = data;
      this.parseStockfish(data?.analysis?.result || '');
      
      // Fetch related videos based on opening recommendations
      if (data?.recommendations?.length > 0) {
        const openingName = data.recommendations[0].split(' - ')[0];
        this.currentOpening = openingName;
        this.fetchVideos(openingName);
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
    })
    .catch(err => {
      this.videos = [];
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
