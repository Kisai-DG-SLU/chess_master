import { ApplicationConfig, provideBrowserGlobalErrorListeners } from '@angular/core';
import { NgxChessBoardModule } from 'ngx-chess-board';

export const appConfig: ApplicationConfig = {
  providers: [
    provideBrowserGlobalErrorListeners(),
    NgxChessBoardModule
  ]
};
