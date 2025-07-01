def bresenham_line(x0, y0, x1, y1):
    """
    Gera uma lista de coordenadas de pontos (pixels) que formam uma linha
    entre (x0, y0) e (x1, y1) usando o algoritmo de Bresenham com inteiros.
    """
    points = [] # Lista que armazenará todos os pontos da linha.
    dx, dy = abs(x1 - x0), abs(y1 - y0) # Calcula a distância total a ser percorrida em cada eixo (delta x e delta y).
                                        # O valor absoluto é usado porque a direção é tratada separadamente.

    sx, sy = 1 if x0 < x1 else -1, 1 if y0 < y1 else -1 # Determina a direção do passo em cada eixo.
                                                        # sx será 1 se a linha for para a direita (x1 > x0) e -1 se for para a esquerda.
                                                        # sy será 1 se a linha for para cima (y1 > y0) e -1 se for para baixo.
    err = dx - dy # É o termo de erro; Ele acumula um valor
                  # que ajuda a decidir quando mover no eixo "menor"
    while True:
        points.append((x0, y0))
        if x0 == x1 and y0 == y1: break # Se o ponto atual for igual ao ponto final, o loop termina.
        e2 = 2 * err # Variável temporária que armazena o dobro do erro.

        if e2 > -dy: # Esta condição verifica se o erro acumulado justifica um passo na direção
                     # do eixo "principal" (o de maior delta).

            err -= dy # Subtrai dy do erro, pois o passo foi "para longe" da linha ideal.
            x0 += sx  # Dá um passo na direção X (seja +1 ou -1).

        if e2 < dx: # Esta condição verifica se o erro acumulado justifica um passo na direção
                    # do eixo "secundário".

            err += dx # Adiciona dx ao erro, pois o passo foi "em direção" à linha ideal.
            y0 += sy # Dá um passo na direção Y (seja +1 ou -1).
            
    return points # Retorna a lista completa de pontos que formam a linha
