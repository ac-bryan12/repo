import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { OlvidoPasswordComponent } from './componentes/pagina_comercial/olvido-password/olvido-password.component';
import { RegistroComponent } from './componentes/pagina_comercial/registro/registro.component';
import { HomeComponent } from './componentes/pagina_comercial/home/home.component';
import { LoginComponent } from './componentes/pagina_comercial/login/login.component';
import { PlanComponent } from './componentes/pagina_comercial/plan/plan.component';
import { ConfirmacionComponent } from './componentes/pagina_comercial/confirmacion/confirmacion.component';
import { EnvInformacionComponent } from './componentes/pagina_comercial/env-informacion/env-informacion.component';
import { CreateCuentaComponent } from './componentes/pagina_comercial/create-cuenta/create-cuenta.component';
import { PagoComponent } from './componentes/pagina_comercial/partials/pago/pago.component';
import { CreacionExitosaComponent } from './componentes/pagina_comercial/creacion-exitosa/creacion-exitosa.component';
import { VistaAdminComponent } from './componentes/sitioAdmin/vista-admin/vista-admin.component';
import { EmpresaComponent } from './componentes/sitioAdmin/empresa/empresa.component';
import { EmpresaTempComponent } from './componentes/sitioAdmin/empresa-temp/empresa-temp.component';
import { PopUpComponent } from './componentes/empresa/pop-up/pop-up.component';
import { AuthGuard } from './services/guards/auth/auth.guard';
import { UtilGuard } from './services/guards/utils/util.guard';
import { GruposPermisosComponent } from './componentes/empresa/grupos-permisos/grupos-permisos.component';
import { AdminGuard } from './services/guards/admin_facturacion/admin.guard';
import { RestablecerPasswordComponent } from './componentes/pagina_comercial/restablecer-password/restablecer-password.component';
import { VistaClienteComponent } from './componentes/cliente/vista-cliente/vista-cliente.component';
import { PerfilComponent } from './componentes/cliente/perfil/perfil.component';
import { ChangePasswordComponent } from './componentes/cliente/change-password/change-password.component';
import { ViewCompanyComponent} from './componentes/empresa/view-company/view-company.component';
import { ProfileUserComponent } from './componentes/empresa/profile-user/profile-user.component';
import { DocumentosCompanyComponent } from './componentes/empresa/documentos-company/documentos-company.component';
import { VistaEmpresaComponent } from './componentes/empresa/vista-empresa/vista-empresa.component';
import { DocumentosComponent } from './componentes/cliente/documentos/documentos.component';
import { EmpresaGuard } from './services/guards/admin_empresa/empresa.guard';
import { ClienteGuard } from './services/guards/cliente/cliente.guard';
import { PageNotFoundComponent } from './componentes/pagina_comercial/pageNotFound/page-not-found.component';
import { GruposEmpresaComponent } from './componentes/empresa/grupos-empresa/grupos-empresa.component';
import { ListGruposComponent } from './componentes/empresa/list-grupos/list-grupos.component';

const routes: Routes = [
  {path:'home',component:HomeComponent},
  {path:'login',component:LoginComponent},
  {path:'registro',component:RegistroComponent},
  {path:'olvido-password',component:OlvidoPasswordComponent},
  {path:'restablecer-password',component:RestablecerPasswordComponent},
  {path:'planes',component:PlanComponent},
  {path:'confirmacion',component:ConfirmacionComponent,canActivate: [UtilGuard]},
  {path:'env-informacion',component:EnvInformacionComponent,canActivate: [UtilGuard]},
  {path:'create-cuenta',component:CreateCuentaComponent},
  {path:'pago',component:PagoComponent},
  //{path:'portal',component:PortalComponent,},
  {path:'',redirectTo:'home',pathMatch:'full'},
  {path:'creacion-exitosa',component:CreacionExitosaComponent,canActivate: [UtilGuard]},
  {path:'portal',component:ViewCompanyComponent,
  children:[
    // {path:'',redirectTo:'empresasTemp',pathMatch:'full'},
    {path:'empresas',component:EmpresaComponent,canActivate: [AdminGuard]},
    {path:'empresasTemp',component:EmpresaTempComponent,canActivate: [AdminGuard]},
    // {path:'cambiar_contrasenia',component:ChangePasswordComponent,canActivate:[AdminGuard]},
    // ]
  // },
  // {path:'cliente',component:VistaClienteComponent},
  // children:[
    {path:'',redirectTo:'cambiar-contrasenia',pathMatch:'full'},
    {path:'perfil',component:PerfilComponent,canActivate:[ClienteGuard]},
    // {path:'cambiar_contrasenia',component:ChangePasswordComponent,canActivate:[ClienteGuard]},
    {path:'documentos',component:DocumentosComponent,canActivate:[ClienteGuard]},
    
  // ]},
  // {path:'view-company',component:ViewCompanyComponent},
  // children:[
    // {path:'',redirectTo:'perfil',pathMatch:'full'},
    {path:'vista-empresa',component:VistaEmpresaComponent,canActivate:[EmpresaGuard]},
    // {path:'profile-user',component:ProfileUserComponent,canActivate:[EmpresaGuard]},
    {path:'documentos-company',component:DocumentosCompanyComponent,canActivate:[EmpresaGuard]},
    {path:'grupos-permisos',component:GruposPermisosComponent,canActivate:[EmpresaGuard]},
    {path:'editarUser',component:PopUpComponent,canActivate:[EmpresaGuard]},
    {path:'grupos',component:ListGruposComponent,canActivate:[EmpresaGuard]},
    {path:'editarGrupos',component:GruposEmpresaComponent,canActivate:[EmpresaGuard]},
    // {path:'perfil',component:PerfilComponent,canActivate:[EmpresaGuard]},
    {path:'cambiar-contrasenia',component:ChangePasswordComponent,canActivate:[EmpresaGuard]},
  ]},
  {path:'**',component:PageNotFoundComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
