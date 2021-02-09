from random import sample, randint
from string import ascii_lowercase
import sqlite3 as sql

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout


kv = """
<Row@RecycleKVIDsDataViewBehavior+BoxLayout>:
    canvas.before:
        Color:
            rgba: 0.5, 0.5, 0.5, 1
        Rectangle:
            size: self.size
            pos: self.pos
            
    Label:
        id: corpo      
    Label:
        id: parametro
    Label:
        id: valor_parametro
    Label:
        id: parametro_ideal
    Label:
        id: unidade

<Test>:
    canvas:
        Color:
            rgba: 0.3, 0.3, 0.3, 1
        Rectangle:
            source: 'agua1.jpg'
            size: self.size
            pos: self.pos
    rv: rv
    orientation: 'vertical'
    GridLayout:
        cols: 2
        rows: 2
        size_hint_y: None
        height: dp(108)
        padding: dp(8)
        spacing: dp(16)
        Button:
            text: 'Limpar'
            on_press: root.clear()
        Button:
            text: 'Ordenar'
            on_press: root.sort()
        TextInput:
            id: new_item_input
            size_hint_x: 0.3
            hint_text: 'Rio Tega...'
            padding: dp(10), dp(10), 0, 0
        BoxLayout:
            spacing: dp(8)
            Button:
                text: 'Buscar'
                on_press: root.insert(new_item_input.text)

    RecycleView:
        id: rv
        scroll_type: ['bars', 'content']
        scroll_wheel_distance: dp(114)
        bar_width: dp(10)
        viewclass: 'Row'
        RecycleBoxLayout:
            default_size: None, dp(56)
            default_size_hint: 1, None
            size_hint_y: None
            height: self.minimum_height
            orientation: 'vertical'
            spacing: dp(10)
"""

Builder.load_string(kv)


class Test(BoxLayout):
    conn = sql.connect('database.sqlite')
    cur  = conn.cursor()


    def busca_parametro(self, busca):
        #Busca parametro
        self.cur.execute("SELECT * FROM dados_coletados WHERE parametro_conforme_artigo LIKE ?", ('%'+busca+'%',))
        rows = self.cur.fetchall()
        return rows
        
    def busca_bacia(self, busca):
        #busca bacia
        self.cur.execute("SELECT * FROM dados_coletados WHERE bacia LIKE ?", ('%'+busca+'%',))
        rows = self.cur.fetchall()
        return rows

    def busca_corpo_hidrico(self, busca):
        #busca corpo hidrico
        self.cur.execute("SELECT * FROM dados_coletados WHERE identificacao_corpo_hidrico LIKE ?", ('%'+busca+'%',))
        rows = self.cur.fetchall()
        return rows

    def busca_municipio(self, busca):
        #busca municipio
        self.cur.execute("SELECT * FROM dados_coletados WHERE municipio LIKE ?", ('%'+busca+'%',))
        rows = self.cur.fetchall()
        return rows

    def busca_parametro_ideal(self, parametro, tipo_agua):
        #busca parametros

        if(tipo_agua == 'Abastecimento'):
            self.cur.execute("SELECT * FROM parametros_abastecimento WHERE parametro LIKE ?", ('%'+parametro+'%',))
            rows = self.cur.fetchall()
            
            try:
                return(rows[0][2])
            
            except IndexError:
                string = parametro.split()        
                self.cur.execute("SELECT * FROM parametros_abastecimento WHERE parametro LIKE ?", ('%'+string[0]+'%',))
                rows = self.cur.fetchall()
                try:
                    return (rows[0][2]) 
                except:
                    return('Sem dados')
        
        if(tipo_agua == 'Subterrânea'):
            self.cur.execute("SELECT * FROM parametros_subterraneas WHERE parametro LIKE ?", ('%'+parametro+'%',))
            rows = self.cur.fetchall()
            
            try:
                return(rows[0][2])
            except IndexError:
                string = parametro.split()        
                self.cur.execute("SELECT * FROM parametros_subterraneas WHERE parametro LIKE ?", ('%'+string[0]+'%',))
                rows = self.cur.fetchall()
                try:
                    return (rows[0][2]) 
                except:
                    return('Sem dados')
            
        if(tipo_agua == 'Superficial'):        
            self.cur.execute("SELECT * FROM parametros_superficiais WHERE parametro LIKE ?", ('%'+parametro+'%',))
            rows = self.cur.fetchall()
            
            try:
                return(rows[0][3])
            except IndexError:
                string = parametro.split()        
                self.cur.execute("SELECT * FROM parametros_superficiais WHERE parametro LIKE ?", ('%'+string[0]+'%',))
                rows = self.cur.fetchall()
                try:
                    return (rows[0][3]) 
                except:
                    return('Sem dados')        
        

        
    def busca_classes_superficiais(self,  busca):

    #---------------------- Dados a serem mostrados da table dados_coletados --------------------
    #identificacao_corpo_hidrico| bacia | municipio | parametro_conforme_artigo | valor        | table parametros | unidade  |
    #        Rio                | bacia | municipio | parametro medido          | valor medido | parametro lei    | unidade  |


    #Busca bacia 
        self.cur.execute("SELECT * FROM classes_superficiais WHERE nome_bacia LIKE ?", ('%'+busca+'%',))
        rows = self.cur.fetchall()
        return rows

    #Busca corpo hidrico
        self.cur.execute("SELECT * FROM classes_superficiais WHERE nome_corpo_hidrico LIKE ?", ('%'+busca+'%',))
        rows = self.cur.fetchall()
        return rows

    #Busca trecho
        self.cur.execute("SELECT * FROM classes_superficiais WHERE trecho LIKE ?", ('%'+busca+'%',))
        rows = self.cur.fetchall()
        return rows

    def busca(self, busca):
    
        if (busca.find('Rio') != -1 or busca.find('rio') != -1 or busca.find('Arroio') != -1 or busca.find('arroio') != -1 or busca.find('Lago') != -1 or busca.find('lago') != -1):
            rows = self.busca_corpo_hidrico(busca)
            
            parametro = rows[0][9]
            trecho = rows[0][8]
            j=0
            k=0
            for i in rows:
                ideal = self.busca_parametro_ideal(i[9],i[21])        
                parametro_atual = i[9]
                trecho_atual = i[8]
      
                if(trecho_atual != '' and j < 9):
                    i = (i[0],i[1],i[2],i[8],i[9],i[11],ideal,i[13],i[21])
                    return rows
                    j = j + 1
                    if(trecho_atual != trecho):
                        trecho = trecho_atual
                        j=0

                if(trecho_atual == '' and k < 16):
                    i = (i[0],i[1],i[2],i[8],i[9],i[11],ideal,i[13],i[21])             
                    return rows
                    k = k + 1

        if (busca.find("Bacia")!= -1 or busca.find("bacia")!= -1):
            rows = self.busca_bacia(busca)

            for i in rows:
                ideal = self.busca_parametro_ideal(i[9],i[21])           
                return(i[0],'|' ,i[1],'|',i[2],'|',i[8],'|',i[9],'|',i[11],'|',ideal,'|',i[13],'|',i[21])
                #return rows


        else:
            rows = self.busca_municipio(busca)
            for i in rows:
                ideal = self.busca_parametro_ideal(i[9],i[21])     
                #return(i[0],'|' ,i[1],'|',i[2],'|',i[8],'|',i[9],'|',i[11],'|',ideal,'|',i[13],'|',i[21])
                #return rows
            
            rows = self.busca_parametro(busca)
            for i in rows:
                ideal = self.busca_parametro_ideal(i[9],i[21])
                return(i[0],'|' ,i[1],'|',i[2],'|',i[8],'|',i[9],'|',i[11],'|',ideal,'|',i[13],'|',i[21])
                #return rows    

    def populate(self):
        self.rv.data = [{'name.text': ''.join(sample(ascii_lowercase, 6)), 'value': str(randint(0, 2000))}for x in range(50)]

    def sort(self):
        self.rv.data = sorted(self.rv.data, key=lambda x: x['name.text'])

    def clear(self):
        self.rv.data = []
        
    #-------------------------------
    def insert(self, value):
        rows = self.busca(value)
        #print(rows)
        self.rv.data = [{'corpo.text': r[0],'parametro.text': r[9],'valor_parametro.text': r[11],'parametro_ideal.text': r[11],'unidade.text': r[13]}for r in rows]
            
        
        #self.rv.data.insert(0, {'name.text': value or 'default value', 'value': 'unknown'})

    def update(self, value):
        if self.rv.data:
            self.rv.data[0]['name.text'] = value or 'default new value'
            self.rv.refresh_from_data()

    def remove(self):
        if self.rv.data:
            self.rv.data.pop(0)


class TestApp(App):
    def build(self):
        return Test()


if __name__ == '__main__':
    TestApp().run()
