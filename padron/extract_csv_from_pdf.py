import os
import fitz
import time

PDF_FOLDER = 'c:/PADRON/PDF_FILES/'
CSV_FOLDER = 'c:/PADRON/CSV_FILES/'

totalPdf = 0
salto = '\n'
log = ''

for base, dirs, files in os.walk(PDF_FOLDER):
    for file in files:
        texto = ''
        doc = fitz.open(PDF_FOLDER+file)
        log = 'Transformando archivo: '+file+' a formato CSV. El archivo tiene '+str(doc.page_count)+' paginas.'
        print(log)
        start = time.time()
        for i in range(0,doc.page_count):
            blocks = [x[4] for x in doc[i].getText("blocks", flags=40)]
            for l in range(157, len(blocks)):
                blocks[l] = blocks[l].replace('\nM\n',' M;').replace('\nV\n',' V;').replace('\n',';')
                
                puntos_comas = blocks[l].count(';')
                indices = [i for i, a in enumerate(blocks[l]) if a == ';']
                if(puntos_comas == 6 and (blocks[l][-2] != 'V' and blocks[l][-2] != 'M' and not blocks[l][-2].isnumeric())):
                    blocks[l] = blocks[l][:indices[2]]+';'+blocks[l][indices[2]:]
                elif(puntos_comas == 5):
                    blocks[l] = blocks[l][:indices[2]]+';'+blocks[l][indices[2]:]
                elif(puntos_comas == 7):
                    blocks[l] = blocks[l][:-1]
                blocks[l] = blocks[l]+salto
                texto = texto + blocks[l]                    
        doc.close()
        f = open(CSV_FOLDER+file[:-4]+'.csv', "w")
        f.write(texto)
        f.close()
        end = time.time()
        log2 = 'Se ha transformado el archivo '+file+f' satisfactioramente\nTiempo de ejecucion: {end-start} '
        log = log + '\n'+log2
        print(log2)
        with open("c:/PADRON/log.txt", "a") as file_object:
            file_object.write(log)