from ROOT import *


mc = "sherpa_MC"
inputvar = "bdt"

dijet_sherpa = TFile("ROOT/dijet_sherpa_py_forGamma_full.root")
#ntrk bins
bin = [0, 50, 100, 150, 200, 300, 400, 500, 600, 800, 1000, 1200, 1500, 2000]
for i in range(13):
    min= bin[i]
    max = bin[i+1]
    #getting data from each bin
    dijet_quark = dijet_sherpa.Get(str(min)+"_LeadingJet_Forward_Quark_"+inputvar)
    dijet_subjetquark = dijet_sherpa.Get(str(min)+"_SubJet_Forward_Quark_"+inputvar)

    dijet_gluon = dijet_sherpa.Get(str(min)+"_LeadingJet_Forward_Gluon_"+inputvar)
    dijet_subjetgluon = dijet_sherpa.Get(str(min)+"_SubJet_Forward_Gluon_"+inputvar)

    dijet_quark2 = dijet_sherpa.Get(str(min)+"_LeadingJet_Central_Quark_"+inputvar)
    dijet_subjetquark2 = dijet_sherpa.Get(str(min)+"_SubJet_Central_Quark_"+inputvar)

    dijet_gluon2 = dijet_sherpa.Get(str(min)+"_LeadingJet_Central_Gluon_"+inputvar)
    dijet_subjetgluon2 = dijet_sherpa.Get(str(min)+"_SubJet_Central_Gluon_"+inputvar)
    dijet_quark.Add(dijet_subjetquark)
    dijet_quark2.Add(dijet_subjetquark2)
    dijet_gluon.Add(dijet_subjetgluon)
    dijet_gluon2.Add(dijet_subjetgluon2)
    dijet_quark.Add(dijet_quark2)
    dijet_gluon.Add(dijet_gluon2)
    
    #normalizing
    
    if(dijet_quark.Integral() != 0):
        dijet_quark.Scale(1./dijet_quark.Integral())
    if(dijet_gluon.Integral() != 0):
        dijet_gluon.Scale(1./dijet_gluon.Integral())
    
    #pick energy bins to plots
    if(min == 50):
        dq50 = dijet_quark
        dg50 = dijet_gluon
        dq50.SetLineColor(1)
        dg50.SetLineColor(1)
    if(min == 100):
        dq100 = dijet_quark
        dg100 = dijet_gluon
        dq100.SetLineColor(3)
        dg100.SetLineColor(3)
    if(min == 150):
        dq150 = dijet_quark
        dg150 = dijet_gluon
        dq150.SetLineColor(6)
        dg150.SetLineColor(6)
    if(min == 200):
        dq200 = dijet_quark
        dg200 = dijet_gluon
        dq200.SetLineColor(2)
        dg200.SetLineColor(2)
    if(min == 300):
        dq300 = dijet_quark
        dg300 = dijet_gluon
        dq300.SetLineColor(4)
        dg300.SetLineColor(4)
    if(min == 400):
        dq400 = dijet_quark
        dg400 =  dijet_gluon
        dq400.SetLineColor(9)
        dg400.SetLineColor(9)
    if(min == 500):
        dq500 = dijet_quark
        dg500 = dijet_gluon
        dq500.SetLineColor(11)
        dg500.SetLineColor(11)

#plotting
def myText(x,y,text,color = 1):
    l = TLatex()
    l.SetTextSize(0.025)
    l.SetNDC()
    l.SetTextColor(color)
    l.DrawLatex(x,y,text)
    pass

c = TCanvas("c","c",500,500)
dq50.Draw("HIST")
dq50.GetXaxis().SetTitle(inputvar)
dq50.GetYaxis().SetLabelSize(0.025)
dq50.GetYaxis().SetTitle("Normalized Entries")

if(inputvar == "bdt"):
    dq50.GetYaxis().SetRangeUser(0,0.1)
    dq50.GetXaxis().SetTitle("BDT")
if(inputvar == "ntrk"):
    dq50.GetYaxis().SetRangeUser(0,0.2)
    dq50.GetXaxis().SetTitle("ntrk")
#dq100.Draw("HIST same")
#dq150.Draw("HIST same")
dq200.Draw("HIST same")
#dq300.Draw("HIST same")
dq400.Draw("HIST same")
#dq500.Draw("HIST same")

dg50.SetLineStyle(2)
#dg100.SetLineStyle(2)
#dg150.SetLineStyle(2)
dg200.SetLineStyle(2)
#dg300.SetLineStyle(2)
dg400.SetLineStyle(2)
#dg500.SetLineStyle(2)
dg50.Draw("h same")
#dg100.Draw("h same")
#dg150.Draw("h same")
dg200.Draw("h same")
#dg300.Draw("h same")
dg400.Draw("h same")
#dg500.Draw("h same")
gStyle.SetOptStat(0)




myText(0.25,0.84,"#it{#bf{#scale[1.6]{#bf{ATLAS} Simulation Preliminary}}}")
myText(0.25,0.80,"#bf{#scale[1.4]{#sqrt{s} = 13 TeV}}")
myText(0.25,0.76,"#bf{#scale[1.4]{Anti-k_{t}, EM+JES R=0.4}}")
myText(0.25,0.72,"#bf{#scale[1.4]{|#eta| < 2.1}}")



legend = TLegend(0.7,0.6,0.9,0.8) ##0.6,0.5,0.9,0.7
legend.SetTextFont(42)
legend.SetFillColor(0)
legend.SetBorderSize(0)
legend.SetFillStyle(0)
legend.SetNColumns(1)

legend.AddEntry(dq50,"Quark","L")
legend.AddEntry(dg50,"Gluon","L")
legend.AddEntry(dq50,"50<p_{T}<100 GeV","F")
#legend.AddEntry(dq100,"100<p_{T}<150 GeV","F")
#legend.AddEntry(dq150,"150<p_{T}<200 GeV","F")
legend.AddEntry(dq200,"200<p_{T}<300 GeV ","F")
#legend.AddEntry(dq300,"300<p_{T}<400 GeV ","F")
legend.AddEntry(dq400,"400<p_{T}<500 GeV ","F")
#legend.AddEntry(dq500,"500<p_{T}<600 GeV ","F")
legend.Draw()
c.Print("./plots//gamma+/dist/dijet_"+inputvar+".pdf")


