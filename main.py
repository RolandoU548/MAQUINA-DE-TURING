from src.MaquinaTuring import MaquinaTuring

if __name__ == "__main__":
    N = int(input())
    maquinas_de_turing = []

    for i in range(N):
        input()
        maquinas_de_turing.append(MaquinaTuring(input()))

    for i in range(N):
        if maquinas_de_turing[i].evaluar_cadena():
            print(f"Caso {i+1}:\nAceptada")
        else:
            print(f"Caso {i+1}:\nRechazada")
