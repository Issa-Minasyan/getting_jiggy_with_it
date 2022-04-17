from flask import Flask, request, url_for, render_template, redirect
import chemparse
import pandas as pd
import matplotlib.pyplot as plt
from jinja2 import Template 

# defining the periodic table
mass_number = {}
with open("info/periodic_table.txt") as f:
    for line in f:
        (key, val) = line.split(    )
        mass_number[key] = float(val)
periodic_table = list(mass_number)


def formula(n):
    return chemparse.parse_formula(n)
alphabe = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ()'


appFlask = Flask(__name__)
@appFlask.route('/log', methods=['GET', 'POST'])
def log():
# handle the POST request
    if request.method == 'POST':
        mix = request.form.get('mix')
        title = mix.replace("+", "-")
        print(title)

        a = mix.split('+')
        mixture = []
        prc = []
        for i in a:
            j = i.lstrip('0123456789.')
            k = i[:3].rstrip(alphabe)
            mixture.append(j)
            prc.append(float(k))
        guns = []
        bullets = []
        for c in range(0, len(mixture)):
            formula_1 = formula(mixture[c])
            comp_const = list(formula_1)
            for i in comp_const:
                guns.append(i)
            for i in comp_const:
                bullets.append(formula_1[i] * prc[c])
        elements = []
        occ = []
        j = 0
        for i in guns:
            if i in elements:
                occ[elements.index(i)] = occ[elements.index(i)] + bullets[j]
                j += 1
                continue
            elements.append(i)
            occ.append(bullets[j])
            j += 1
        def f(n):
            return occ[n]/sum(occ)
        ratio = []
        for i in range(0, len(occ)):
            ratio.append(f(i))
            i += 1
        Z = []
        for i in range(0, len(elements)):
            Z.append(periodic_table.index(elements[i]) + 1)
            i =+ 1
        energy = request.form.get('energy')
        b = energy.split()
        energies = []
        for i in b:
            energies.append(float(i))
        energies.sort(reverse=False)
        zeff = []
        # finding Z-eff for each given energy
        for k in energies:
            u = []
        # accessing the files
            for i in Z:
                websites = pd.read_csv("info/{:s}.txt".format(str(i)),
                                       delimiter = '\t', header = None)
                websites.columns = ['Photon-Energy (MeV)', 'Coh. Scatt.',
                                    'incoh. scatt.', 'photoelectric', 'Nuclear PP',
                                    'Electron PP','Tot. w/', 'Tot. w/o', 'extra slot']
                websites.to_csv('info/test.csv', index = None)
                websites_output = pd.read_csv('info/test.csv')
                photon_str = list(websites['Photon-Energy (MeV)'][2:])
                photon = [float(x) for x in photon_str]
                MAC_str = list(websites['Tot. w/'][2:])
                MAC = [float(x) for x in MAC_str]
        # finding miu
                index = photon.index(k)
                miu = MAC[index]
                u.append(miu)
        # calculation
            num = []
            den = []

            for n in range(0, len(elements)):
                a = f(n) * mass_number[elements[n]] * u[n]
                num.append(a)
            for m in range(0, len(elements)):
                b = f(m) * (mass_number[elements[m]]/Z[m]) * u[m]
                den.append(b)
            Z_effective = sum(num)/sum(den)
            zeff.append(Z_effective)


        

        plt.switch_backend('agg')
        plt.plot(energies, zeff)
        plt.xlabel("Energy (MeV)")
        plt.ylabel("Z_effective")
        plt.savefig('static/graph.png')


        




        joey = "Energy (MeV)\t\t\tZ-eff\n"
        with open('info/silly.txt', 'w') as f:
            for i in range(0, len(energies)):
                f.write("{}\t\t\t\t{}\n".format(energies[i], zeff[i]))
        f.close()
        with open('info/silly.txt', 'r') as g:
            lines = g.read()
        g.close()


        moto = "Compound\t\t\t%\n"
        with open('info/dummy.txt', 'w') as h:
            for i in range(0, len(mixture)):
                h.write("{}\t\t\t\t{}\n".format(mixture[i], prc[i]))
        h.close()
        with open('info/dummy.txt', 'r') as j:
            cards = j.read()
        j.close()


        yugi = "Element\t\t\t\tRatio (total = 1)\n"
        with open('info/airhead.txt', 'w') as l:
            for i in range(0, len(elements)):
                l.write("{}\t\t\t\t{}\n".format(elements[i], ratio[i]))
        l.close()
        with open('info/airhead.txt', 'r') as w:
            deck = w.read()
        w.close()        


      
        return redirect(url_for("user", usr=title))

# otherwise handle the GET request
    else:
        return render_template("index.html")

@appFlask.route("/<usr>")
def user(usr):
    joey = "Energy (MeV)\t\t\tZ-eff\n"
    
    with open('info/silly.txt', 'r') as g:
        lines = g.read()
    g.close()
    return render_template("answer.html", joey=joey, lines=lines)   #, moto=moto, cards=cards, yugi=yugi, deck=deck)


if __name__ == '__main__':
    appFlask.run(debug = True)
