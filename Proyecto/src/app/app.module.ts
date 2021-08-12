import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HomeComponent } from './home/home.component';
import { LoginComponent } from './login/login.component';
import { NavComponent } from './componentes/pagina_comercial/nav/nav.component';
import { RegistroComponent } from './componentes/pagina_comercial/registro/registro.component';
import { OlvidoPasswordComponent } from './componentes/pagina_comercial/olvido-password/olvido-password.component';

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    LoginComponent,
    NavComponent,
    RegistroComponent,
    OlvidoPasswordComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
