import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { OlvidoPasswordComponent } from './componentes/pagina_comercial/olvido-password/olvido-password.component';
import { RegistroComponent } from './componentes/pagina_comercial/registro/registro.component';
import { HomeComponent } from './home/home.component';
import { LoginComponent } from './login/login.component';

const routes: Routes = [
  {path:'home',component:HomeComponent},
  {path:'login',component:LoginComponent},
  {path:'registro',component:RegistroComponent},
  {path:'olvido-password',component:OlvidoPasswordComponent},
  {path:'',redirectTo:'home',pathMatch:'full'}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
