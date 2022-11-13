class TiempoEnAños_Meses_Dias():
    def __init__(self, es_perpetua:bool=False, _años:int=0, _meses:int=0, _dias:int=0):
        self.perpetua = es_perpetua
        self.años = _años
        self.meses = _meses
        self.dias = _dias

        if self.perpetua:
            self.años = self.meses = self.dias = 0
    
    def __str__(self):
        if self.perpetua:
            return 'Es una pena perpetua'        
        return '...{} año(s), {} mes(es) y {} día(s)...'.format(self.años, self.meses, self.dias)

class MontoDePena(TiempoEnAños_Meses_Dias):
    def __init__(self, es_perpetua: bool = False, _años: int = 0, _meses: int = 0, _dias: int = 0, reclArt52:bool=False):
        super().__init__(es_perpetua, _años, _meses, _dias)
        self._reclArt52 = reclArt52

    def __str__(self):
        if self.perpetua:
            return 'Es una pena perpetua'        
        if self._reclArt52:
            return 'Es una reclusión por tiempo indeterminado'
        return '...{} año(s), {} mes(es) y {} día(s)...'.format(self.años, self.meses, self.dias)

x = MontoDePena(reclArt52=True)
y = MontoDePena(_años=3)


print(x)
print(y)