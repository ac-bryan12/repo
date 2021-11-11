import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HomeComponent } from './componentes/pagina_comercial/home/home.component';
import { LoginComponent } from './componentes/pagina_comercial/login/login.component';
import { NavComponent } from './componentes/pagina_comercial/partials/nav/nav.component';
import { PlanComponent } from './componentes/pagina_comercial/plan/plan.component';
import { ComparePlanComponent } from './componentes/pagina_comercial/partials/compare-plan/compare-plan.component';
import { RegistroComponent } from './componentes/pagina_comercial/registro/registro.component';
import { OlvidoPasswordComponent } from './componentes/pagina_comercial/olvido-password/olvido-password.component';
import { HttpClientModule, HttpClientXsrfModule } from '@angular/common/http';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { ConfirmacionComponent } from './componentes/pagina_comercial/confirmacion/confirmacion.component';
import { EnvInformacionComponent } from './componentes/pagina_comercial/env-informacion/env-informacion.component';
import { CreateCuentaComponent } from './componentes/pagina_comercial/create-cuenta/create-cuenta.component';
import { PagoComponent } from './componentes/pagina_comercial/partials/pago/pago.component';
import { CreacionExitosaComponent } from './componentes/pagina_comercial/creacion-exitosa/creacion-exitosa.component';
import { VistaAdminComponent } from './componentes/sitioAdmin/vista-admin/vista-admin.component';
import { EmpresaComponent } from './componentes/sitioAdmin/empresa/empresa.component';
import { NavAdminComponent } from './componentes/sitioAdmin/partials/nav-admin/nav-admin.component';
import { HeaderComponent } from './componentes/sitioAdmin/partials/header/header.component';
import { EmpresaTempComponent } from './componentes/sitioAdmin/empresa-temp/empresa-temp.component';
import { PopUpComponent } from './componentes/sitioAdmin/pop-up/pop-up.component';
import { CookieService } from 'ngx-cookie-service';
import { PortalComponent } from './componentes/pagina_comercial/portal/portal.component';
import { VistaEmpresaComponent } from './componentes/sitioAdmin/vista-empresa/vista-empresa.component';
import { GruposPermisosComponent } from './componentes/sitioAdmin/grupos-permisos/grupos-permisos.component';
import { RestablecerPasswordComponent } from './componentes/pagina_comercial/restablecer-password/restablecer-password.component';
import { NavClientComponent } from './componentes/cliente/nav-client/nav-client.component';
import { HeaderClientComponent } from './componentes/cliente/header-client/header-client.component';
import { VistaClienteComponent } from './componentes/cliente/vista-cliente/vista-cliente.component';
import { DocumentosComponent } from './componentes/cliente/documentos/documentos.component';
import { PerfilComponent } from './componentes/cliente/perfil/perfil.component';
import { ChangePasswordComponent } from './componentes/cliente/change-password/change-password.component';

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
    CreacionExitosaComponent,
    VistaAdminComponent,
    EmpresaComponent,
    NavAdminComponent,
    HeaderComponent,
    EmpresaTempComponent,
    PopUpComponent,
    PortalComponent,
    VistaEmpresaComponent,
    GruposPermisosComponent,
    RestablecerPasswordComponent,
    NavClientComponent,
    HeaderClientComponent,
    VistaClienteComponent,
    DocumentosComponent,
    PerfilComponent,
    ChangePasswordComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule,
    ReactiveFormsModule
  ],
  providers: [CookieService],
  bootstrap: [AppComponent]
})
export class AppModule { }
