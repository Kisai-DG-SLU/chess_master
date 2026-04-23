import { Component, ViewChild, OnInit, HostListener, ElementRef, ChangeDetectorRef, ViewEncapsulation } from '@angular/core';
import { RouterModule } from '@angular/router';
import { NgxChessBoardComponent, NgxChessBoardService } from 'ngx-chess-board';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
  encapsulation: ViewEncapsulation.None,
  standalone: true,
  imports: [RouterModule, NgxChessBoardComponent]
})
export class AppComponent implements OnInit {
  @ViewChild('board', { static: false }) board!: NgxChessBoardComponent;
  playerLevel = 'intermediate';
  analysisResult: string = '';

  constructor(private ngxChessBoardService: NgxChessBoardService) {}

  ngOnInit() {}

  resetBoard() {
    if (this.board) {
      this.board.reset();
    }
  }

  setPosition(fen: string) {
    if (this.board) {
      this.board.setFEN(fen);
    }
  }

  setRuyLopez() {
    this.setPosition('r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3');
  }

  setSicilian() {
    this.setPosition('rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKB1R w KQkq c6 0 2');
  }

  analyzePosition() {
    if (this.board) {
      const fen = this.board.getFEN();
      
      fetch('http://localhost:8000/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          position: fen,
          player_level: this.playerLevel
        })
      .then(res => res.json())
      .then(data => {
        this.analysisResult = JSON.stringify(data, null, 2);
      })
      .catch(err => {
        this.analysisResult = 'Erreur: ' + err.message;
      });
    }
  }
}
