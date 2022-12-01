from enum import Enum

class LC_KEYS(Enum):    
    _fechaImplementacion_YEAR_KEY = 'Fecha de implementacion - year'
    _fechaImplementacion_MONTH_KEY = 'Fecha de implementacion - month'
    _fechaImplementacion_DAY_KEY = 'Fecha de implementacion - day'    
    _requisitoTemporalPenaPerpetua_KEY = 'Requisito temporal pena perpetua'
    _ask_esReincidente_KEY = 'Preguntar si es reincidente'
    _ask_siHayAccesoria52 = 'Preguntar si hay accesoria del 52 CP'
    _ask_esComputoPorLCRevocada_KEY = 'Preguntar si es un computo por LC revocada'
    _ask_delitosExcluidos25892_KEY = 'Preguntar por delitos excluidos ley 25.892'
    _ask_delitosExcluidos27375_KEY = 'Preguntar por delitos excluidos ley 27.375'
    _ask_2_3ConCalifBUENO_KEY = 'Preguntar por 2/3 con calificacion BUENO'

class LC_REGIMENES(Enum):    
    _Ley_11179 = 'Ley 11.179'
    _Ley_25892 = 'Ley 25.892'
    _Ley_27375 = 'Ley 27.375'

class ST_KEYS(Enum):    
    _fechaImplementacion_YEAR_KEY = 'Fecha de implementacion - year'
    _fechaImplementacion_MONTH_KEY = 'Fecha de implementacion - month'
    _fechaImplementacion_DAY_KEY = 'Fecha de implementacion - day' 
    _ask_siHayAccesoria52 = 'Preguntar si hay accesoria del 52 CP'
    _ask_esComputoPorEvasionDeST_KEY = 'Preguntar si es un computo por evasion de ST'
    _ask_delitosExcluidos25948_KEY = 'Preguntar por delitos excluidos por 56 bis ley 25.948'
    _ask_delitosExcluidos27375_KEY = 'Preguntar por delitos excluidos por 56 bis ley 27.375'
    _ask_siEstaPeriodoDePruebaYDesdeCuando = 'Preguntar si se encuentra en periodo de prueba, y desde cuando'
    _ask_requisitoDeCalificacion = 'Preguntar por requisito de calificacion'   

class ST_REGIMENES(Enum):    
    _DecretoLey412_58 = 'Decreto Ley 412/58'
    _Ley_24660 = 'Ley 24.660'
    _Ley_25948 = 'Ley 25.948'
    _Ley_27375 = 'Ley 27.375'

class ST_COMPUTO_27375_SITUACION(Enum):    
    NO_HAY_COMPUTO_CALCULADO = 0
    ES_ANTERIOR_A_LEY_27375 = 1
    HAY_COMPUTO = 2
    TODAVIA_NO_INGRESO_A_PERIODO_DE_PRUEBA = 3
    INGRESO_A_PERIODO_DE_PRUEBA = 4

class LA_KEYS(Enum):    
    _fechaImplementacion_YEAR_KEY = 'Fecha de implementacion - year'
    _fechaImplementacion_MONTH_KEY = 'Fecha de implementacion - month'
    _fechaImplementacion_DAY_KEY = 'Fecha de implementacion - day'
    _requisitoTemporal_KEY = 'Requisito temporal'
    _ask_nuevoComputoLArevoc_KEY = 'Preguntar si es nuevo computo por libertad revocada'
    _ask_delitosExcluidos25948_KEY = 'Preguntar por delitos excluidos por 56 bis ley 25.948'
    _ask_delitosExcluidos27375_KEY = 'Preguntar por delitos excluidos por 56 bis ley 27.375'

class LA_REGIMENES(Enum):    
    _Ley_24660 = 'Ley 24.660'
    _Ley_25948 = 'Ley 25.948'
    _Ley_27375 = 'Ley 27.375'

class REGPREPLIB_KEYS(Enum):    
    _fechaImplementacion_YEAR_KEY = 'Fecha de implementacion - year'
    _fechaImplementacion_MONTH_KEY = 'Fecha de implementacion - month'
    _fechaImplementacion_DAY_KEY = 'Fecha de implementacion - day'
    _ask_delitosExcluidos27375_KEY = 'Preguntar por delitos excluidos por 56 bis ley 27.375'

class REGPREPLIB_REGIMENES(Enum):    
    _Ley_27375 = 'Ley 27.375'