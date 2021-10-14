import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Validacion } from 'src/assets/Validacion';

@Component({
  selector: 'change-password',
  templateUrl: './change-password.component.html',
  styleUrls: ['./change-password.component.css']
})
export class ChangePasswordComponent implements OnInit {
  public changePassword: FormGroup;
  public validate: Validacion = new Validacion();
  constructor(
    private fb: FormBuilder
  ) {
    this.changePassword = this.fb.group({
      actualpassword: this.fb.control('', [Validators.required]),
      password: this.fb.control('', [Validators.required, Validators.pattern('^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[_.{}=<>;:,\+$@$!%*?&])[A-Za-z\d_.{}=<>;:,\+$@$!%*?&].{7,}')]),
      confpassword: this.fb.control('', [Validators.required, Validators.pattern('^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[_.{}=<>;:,\+$@$!%*?&])[A-Za-z\d_.{}=<>;:,\+$@$!%*?&].{7,}')])
    })
  }

  ngOnInit(): void {
  }

  validacionPassword() {
    return this.validate.validarConfPassword(this.changePassword.get('password')?.value, this.changePassword.get('confpassword')?.value)
  }
}
