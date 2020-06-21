from ROOT import *
import numpy as np
ntrackall =TFile("ROOT/dijet_sherpa_py_forGamma_full.root")
gammaFile = TFile("ROOT/gammajet_sherpa.root")

data = "gamma"
inputvar = "eta"

def myText(x,y,text,color =1):
    l = TLatex()
    l.SetTextSize(0.025)
    l.SetTextColor(color)
    l.DrawLatex(x,y,text)
    pass

p1 = np.array([0.01,0.99])
p2 = np.array([0.99,0.01])
c = TCanvas("c","c",500,500)
c.SetGrid()
bin = [0,50,100,150,200,300,400,500,600]
#bin = [0.0,0.5,1.0,2.1]
grparams = []
for i in range(len(bin)-1):
    min = bin[i]
    max = bin[i+1]
    x = np.empty(100)
    y = np.empty(100)
       
    c = TCanvas("c","c",500,500)
    c.SetGrid()
    if(data == "dijet"):
        dijet_quark = ntrackall.Get(str(min)+"_LeadingJet_Forward_Quark_"+inputvar)
        dijet_subjetquark = ntrackall.Get(str(min)+"_SubJet_Forward_Quark_"+inputvar)

        dijet_gluon = ntrackall.Get(str(min)+"_LeadingJet_Forward_Gluon_"+inputvar)
        dijet_subjetgluon = ntrackall.Get(str(min)+"_SubJet_Forward_Gluon_"+inputvar)

        dijet_quark2 = ntrackall.Get(str(min)+"_LeadingJet_Central_Quark_"+inputvar)
        dijet_subjetquark2 = ntrackall.Get(str(min)+"_SubJet_Central_Quark_"+inputvar)

        dijet_gluon2 = ntrackall.Get(str(min)+"_LeadingJet_Central_Gluon_"+inputvar)
        dijet_subjetgluon2 = ntrackall.Get(str(min)+"_SubJet_Central_Gluon_"+inputvar)

        for a in range(60):
            if np.isnan(dijet_quark.GetBinContent(a)):
                dijet_quark.SetBinContent(a,0)
            if np.isnan(dijet_quark2.GetBinContent(a)):
                dijet_quark2.SetBinContent(a,0)

        dijet_quark.Add(dijet_quark2)
    


        for b in range(60):
            if np.isnan(dijet_gluon.GetBinContent(b)):
                dijet_gluon.SetBinContent(b,0)
            if np.isnan(dijet_gluon2.GetBinContent(b)):
                dijet_gluon2.SetBinContent(b,0)

        dijet_gluon.Add(dijet_gluon2)
    

        for a in range(60):
            if np.isnan(dijet_subjetquark.GetBinContent(a)):
                dijet_subjetquark.SetBinContent(a,0)
            if np.isnan(dijet_subjetquark2.GetBinContent(a)):
                dijet_subjetquark2.SetBinContent(a,0)

        dijet_subjetquark.Add(dijet_subjetquark2)

        for a in range(60):
            if np.isnan(dijet_subjetgluon.GetBinContent(a)):
                dijet_subjetgluon.SetBinContent(a,0)
            if np.isnan(dijet_subjetgluon2.GetBinContent(a)):
                dijet_subjetgluon2.SetBinContent(a,0)
        dijet_subjetgluon.Add(dijet_subjetgluon2)


        dijet_quark.Add(dijet_subjetquark)
        dijet_gluon.Add(dijet_subjetgluon)

        if(dijet_quark.Integral() != 0):
            dijet_quark.Scale(1./dijet_quark.Integral())
        if(dijet_gluon.Integral() != 0):
            dijet_gluon.Scale(1./dijet_gluon.Integral())


    
        for i in range(100):
            x[i] = dijet_quark.Integral(0,i)
            y[i] = 1- dijet_gluon.Integral(0,i)
        
    if(data == "gamma"):
        gamma_centralquark = gammaFile.Get(str(min)+"_LeadingJet_Central_Quark_"+inputvar)
        gamma_centralgluon = gammaFile.Get(str(min)+"_LeadingJet_Central_Gluon_"+inputvar)
        if(gamma_centralquark.Integral() != 0):
            gamma_centralquark.Scale(1./gamma_centralquark.Integral())
        if(gamma_centralgluon.Integral() != 0):
            gamma_centralgluon.Scale(1./gamma_centralgluon.Integral())
        

        for i in range(100):
            x[i] = gamma_centralquark.Integral(0,i)
            y[i] = 1 - gamma_centralgluon.Integral(0,i)

    grparams.append(x)
    grparams.append(y)

g1 = TGraph(100,grparams[0],grparams[1]) #0-50
g1.SetLineColor(1)
g2 = TGraph(100,grparams[2],grparams[3]) #50-100
g2.SetLineColor(2)
g3 = TGraph(100,grparams[4],grparams[5]) #100-150
g3.SetLineColor(2)
g4 = TGraph(100,grparams[6], grparams[7]) #150 -200
g4.SetLineColor(2)
g5 = TGraph(100,grparams[8], grparams[9]) #200-300
g5.SetLineColor(3)
g6 = TGraph(100,grparams[10], grparams[11]) #300-400
g6.SetLineColor(4)
g7 = TGraph(100,grparams[12],grparams[13]) #400-500
g7.SetLineColor(4)
g8 = TGraph(2,p1,p2)
g8.SetLineColor(1)
g8.SetLineStyle(2)
g1.SetLineWidth(1)
g2.SetLineWidth(1)
g3.SetLineWidth(1)
g1.Draw()
#g2.Draw("same")
g3.Draw("same")
#g8.Draw("same")
#g4.Draw("same")
g5.Draw("same")
#g6.Draw("same")
g7.Draw("same")
g8.Draw("same")
gPad.SetTickx()
gPad.SetTicky()
gStyle.SetGridStyle(2)
gStyle.SetGridColor(15)
legend = TLegend(0.15,0.32,0.45,0.52)
legend.SetTextFont(42)
legend.SetFillColor(0)
legend.SetBorderSize(0)
legend.SetFillStyle(0)
legend.SetNColumns(1)

myText(0.10,0.18,"#it{#bf{#scale[1.4]{#bf{ATLAS} Simulation Preliminary}}}")
myText(0.10,0.14,"#bf{#scale[1.2]{#sqrt{s} = 13 TeV}}")
myText(0.10,0.10,"#bf{#scale[1.2]{Anti-k_{t}, EM+JES R=0.4}}")
myText(0.10,0.06,"#bf{#scale[1.2]{|#eta| < 2.1}}")

g1.SetTitle("")
g1.GetXaxis().SetTitle("Quark Efficiency")
g1.GetYaxis().SetTitle("Gluon Rejection")
g1.GetXaxis().SetLimits(0,1)
g1.SetMinimum(0)
g1.SetMaximum(1)
if(inputvar == "ntrk"):
    legend.SetHeader("Quark Jet Tagging: n_{track} < X" , "C")
elif(inputvar == "bdt"):
    legend.SetHeader("Quark Jet Tagging: bdt <X","C")
legend.SetTextSize(0.03)
#legend.SetHeader("ntrk: 300<\ p_{T}<400 GeV", "C")
#legend.AddEntry(g1,"0 < \eta < 0.5","L")
legend.AddEntry(g1,"0 < p_{T} < 50 GeV","L")
legend.AddEntry(g3,"100 < p_{T} < 150 GeV","L")
#legend.AddEntry(g2,"0.5 < \eta < 1","L")
#legend.AddEntry(g3,"1 < \eta < 2.1 ","L")
#legend.AddEntry(g4, "150 < p_{T} < 200 GeV", "L")
legend.AddEntry(g5, "200 < p_{T} < 300 GeV", "L")
#legend.AddEntry(g6, "300 < p_{T} < 400 GeV", "L")
legend.AddEntry(g7, "400 < p_{T} > 500 GeV", "L")
legend.Draw()

if(data == "dijet"):
    c.Print("./plots/gamma+/ROC_plots_var/ROC_" + inputvar + "_dijet.pdf")
if(data == "gamma"):
    c.Print("./plots/gamma+/ROC_plots_var/ROC_" + inputvar + "_gamma.pdf")

