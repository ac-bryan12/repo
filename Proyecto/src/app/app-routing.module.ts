import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { OlvidoPasswordComponent } from './componentes/pagina_comercial/olvido-password/olvido-password.component';
import { RegistroComponent } from './componentes/pagina_comercial/registro/registro.component';
import { HomeComponent } from './home/home.component';
import { LoginComponent } from './login/login.component';
import { PlanComponent } from './componentes/pagina_comercial/plan/plan.component';
import { ConfirmacionComponent } from './componentes/pagina_comercial/confirmacion/confirmacion.component';
import { EnvInformacionComponent } from './componentes/pagina_comercial/env-informacion/env-informacion.component';
import { CreateCuentaComponent } from './componentes/pagina_comercial/create-cuenta/create-cuenta.component';
import { PagoComponent } from './componentes/pagina_comercial/pago/pago.component';

const routes: Routes = [
  {path:'home',component:HomeComponent},
  {path:'login',component:LoginComponent},
  {path:'registro',component:RegistroComponent},
  {path:'olvido-password',component:OlvidoPasswordComponent},
  {path:'planes',component:PlanComponent},
  {path:'confirmacion',component:ConfirmacionComponent},
  {path:'env-informacion',component:EnvInformacionComponent},
  {path:'create-cuenta',component:CreateCuentaComponent},
  {path:'pago',component:PagoComponent},
  {path:'',redirectTo:'home',pathMatch:'full'}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
