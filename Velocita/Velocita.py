import ac
import acsys

# Declarando as variáveis globais
velocidade_label = None
contagem_ativa = False
tempo_contagem = 0.0

def get_gear_name(gear_value):
    if gear_value == 0:
        return "R"
    elif gear_value == 1:
        return "N"
    elif gear_value == 2:
        return "1"
    elif gear_value == 3:
        return "2"
    elif gear_value == 4:
        return "3"
    elif gear_value == 5:
        return "4"
    elif gear_value == 6:
        return "5"
    elif gear_value == 7:
        return "6"
    elif gear_value == 8:
        return "7"
    elif gear_value == 9:
        return "8"
    elif gear_value > 1:
        return str(int(gear_value))  # Converte para inteiro para remover casas decimais
    else:
        return "Unknown"

def acMain(ac_version):
    global velocidade_label
    
    appWindow = ac.newApp("Velocidade")
    ac.setSize(appWindow, 400, 100)

    velocidade_label = ac.addLabel(appWindow, "Velocidade: 0 km/h\nSegundos de 0 a 100: 0.0 s\nMarcha: ")
    ac.setPosition(velocidade_label, 30, 30)

    return "Velocidade"

def acUpdate(deltaT):
    global velocidade_label, contagem_ativa, tempo_contagem
    
    if velocidade_label:
        velocidade_kph = ac.getCarState(0, acsys.CS.SpeedKMH)
        velocidade_label_text = "Velocidade: {:.1f} km/h".format(velocidade_kph)
        
        # Obtém a marcha atual do carro
        marcha_atual = ac.getCarState(0, acsys.CS.Gear)
        
        # Corrigindo o valor da marcha para refletir corretamente
        if marcha_atual > 1:
            marcha_corrigida = int(marcha_atual)
        else:
            marcha_corrigida = marcha_atual
        
        marcha_texto = "Marcha: {}".format(get_gear_name(marcha_corrigida))
        
        # Verifica se a contagem deve iniciar
        if velocidade_kph > 0 and not contagem_ativa:
            contagem_ativa = True
        
        # Verifica se a contagem deve parar
        if velocidade_kph >= 100:
            contagem_ativa = False
        
        # Reinicia a contagem se a velocidade cair abaixo de 1 km/h
        if velocidade_kph < 1:
            contagem_ativa = False
            tempo_contagem = 0.0
        
        # Se a contagem está ativa, incrementa o tempo
        if contagem_ativa:
            tempo_contagem += deltaT
        
        # Mostra o tempo de contagem e a marcha na interface
        tempo_contagem_text = "Segundos de 0 a 100:   {:.1f} s".format(tempo_contagem)
        ac.setText(velocidade_label, velocidade_label_text + "\n" + tempo_contagem_text + "\n" + marcha_texto)
