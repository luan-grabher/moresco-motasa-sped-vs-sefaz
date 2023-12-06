from easygui import fileopenbox, msgbox

def getArquivoSpedFromUser():
    msgbox('Selecione o arquivo txt do relatório do SPED com as notas')

    return fileopenbox(msg='Selecione o arquivo txt do relatório do SPED com as notas',
                       title='Relatório txt do SPED',
                       default='*.txt',
                       filetypes='*.txt',
                       multiple=False)