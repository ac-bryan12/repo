import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HomeComponent } from './home/home.component';
import { LoginComponent } from './login/login.component';
import { NavComponent } from './componentes/pagina_comercial/nav/nav.component';
import { PlanComponent } from './componentes/pagina_comercial/plan/plan.component';
import { ComparePlanComponent } from './componentes/pagina_comercial/compare-plan/compare-plan.component';
import { RegistroComponent } from './componentes/pagina_comercial/registro/registro.component';
import { OlvidoPasswordComponent } from './componentes/pagina_comercial/olvido-password/olvido-password.component';
import { ConfirmacionComponent } from './componentes/pagina_comercial/confirmacion/confirmacion.component';
import { EnvInformacionComponent } from './componentes/pagina_comercial/env-informacion/env-informacion.component';
import { CreateCuentaComponent } from './componentes/pagina_comercial/create-cuenta/create-cuenta.component';
import { PagoComponent } from './componentes/pagina_comercial/pago/pago.component';

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    LoginComponent,
    NavComponent,
    PlanComponent,
    ComparePlanComponent,
    RegistroComponent,
    OlvidoPasswordComponent,
    ConfirmacionComponent,
    EnvInformacionComponent,
    CreateCuentaComponent,
    PagoComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
