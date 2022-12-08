def _CalcularRegimenPreparacionLibertad(self):
        
        # Utiliza las siguientes variables:
        # - _vencimientoDePena  

        if self._regimen_normativo._regimen_PREPLIB == REGPREPLIB_REGIMENES._No_aplica.value:
            return 

        if self._monto_de_pena.perpetua:
            return                     
        
        if self._regimen_normativo._regimen_PREPLIB == REGPREPLIB_REGIMENES._Ley_27375.value:

            _computo_regPrepLib = self._vencimiento_de_pena
            _computo_regPrepLib += relativedelta(years=-1)            
        
            # No se resta acá las otras detenciones porque ya fueron restadas en el vencimiento de pena

            print(f'DEBUG: Régimen de preparación para la libertad sin aplicar estímulo educativo = {Datetime_date_enFormatoXX_XX_XXXX(_computo_regPrepLib)}')
            # Aplica el estímulo educativo, si hay
            _computo_regPrepLib = self._AplicarEstimuloEducativo(_computo_regPrepLib, self._estimulo_educativo)        

            # Guarda el dato en la variable correspondiente
            self._regimen_preparacion_libertad_COMPUTO = _computo_regPrepLib