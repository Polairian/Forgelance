
BuffLanceIncendiaire = 4
PA = 12

initial_state = (0, 0, False)
DSorts, BuffLanceIncendiaireTotal, Lance = initial_state

def LanceIncendiaire():
    global Lance, DSorts, BuffLanceIncendiaireTotal
    Lance = False
    DSorts += BuffLanceIncendiaireTotal + 19  # (18+20)/2
    BuffLanceIncendiaireTotal = 0

def apply_sort(damage, buff=0, proc=False, muspel=False):
    global Lance, DSorts, BuffLanceIncendiaireTotal
    DSorts += damage
    BuffLanceIncendiaireTotal += buff
    if proc:
        if Lance:
            LanceIncendiaire()
        elif not muspel:
            Lance = True

def LanceAIncendie(): apply_sort(24.5, proc=True)
def MoulinRouge(): apply_sort(30, BuffLanceIncendiaire)
def Fente(): apply_sort(13, BuffLanceIncendiaire)
def FerRouge(): apply_sort(28.5, BuffLanceIncendiaire // 2)
def EstocBrulant(): apply_sort(26.5, BuffLanceIncendiaire)
def Muspel(): apply_sort(33, proc=True, muspel=True)
def Maelstom(): apply_sort(26.5, proc=True)

Sorts = [LanceAIncendie, MoulinRouge, Fente, FerRouge, EstocBrulant, Muspel, Maelstom]
limits = [3, 2, 2, 3, 3, 2, 3]
pa_costs = [3, 3, 2, 3, 3, 4, 3]

def get_seq_from(pa, current_limits: list):
    for i, (f, limit, cost) in enumerate(zip(Sorts, current_limits, pa_costs)):
        if current_limits[i] > 1 and cost <= pa:
            new_limits = current_limits.copy()
            new_limits[i] -= 1
            yield [i]
            for subseq in get_seq_from(pa - cost, new_limits):
                yield [i, *subseq]

def simulate_turns():
    global Lance, DSorts, BuffLanceIncendiaireTotal
    tours = []

    for seq in get_seq_from(PA, limits.copy()):
        DSorts, BuffLanceIncendiaireTotal, Lance = initial_state

        for idx in seq:
            Sorts[idx]()
        tours.append((*seq, DSorts))

    return tours

tours = simulate_turns()

tours.sort(key=lambda x:-x[-1])
print(*tours[:5], sep='\n')
