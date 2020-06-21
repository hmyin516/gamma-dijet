from ROOT import *


mc = "sherpa_MC"
inputvar = "ntrk"

gamma_sherpa = TFile("ROOT/gammajet_sherpa.root")
#ntrk bins
bin = [0, 50, 100, 150, 200, 300, 400, 500, 600, 800, 1000, 1200, 1500, 2000]
for i in range(13):
    min= bin[i]
    max = bin[i+1]
    #getting data from each bin
    gamma_centralquark = gamma_sherpa.Get(str(min)+"_LeadingJet_Central_Quark_"+inputvar)
    gamma_centralgluon = gamma_sherpa.Get(str(min)+"_LeadingJet_Central_Gluon_"+inputvar)
    
    #normalizing
    if(gamma_centralquark.Integral() != 0):
        gamma_centralquark.Scale(1./gamma_centralquark.Integral())
    if(gamma_centralgluon.Integral() != 0):
        gamma_centralgluon.Scale(1./gamma_centralgluon.Integral())
    #picking 3 low energy bins to plot
    if(min == 50):
        gcq50 = gamma_centralquark
        gcg50 = gamma_centralgluon
        gcq50.SetLineColor(1)
        gcg50.SetLineColor(1)
    if(min == 100):
        gcq100 = gamma_centralquark
        gcg100 = gamma_centralgluon
        gcq100.SetLineColor(3)
        gcg100.SetLineColor(3)
    if(min == 150):
        gcq150 = gamma_centralquark
        gcg150 = gamma_centralgluon
        gcq150.SetLineColor(6)
        gcg150.SetLineColor(6)
    if(min == 200):
        gcq200 = gamma_centralquark
        gcg200 = gamma_centralgluon
        gcq200.SetLineColor(2)
        gcg200.SetLineColor(2)
    if(min == 300):
        gcq300 = gamma_centralquark
        gcg300 = gamma_centralgluon
        gcg300.SetLineColor(4)
        gcg300.SetLineColor(4)
    if(min == 400):
        gcq400 = gamma_centralquark
        gcg400 =  gamma_centralgluon
        gcq400.SetLineColor(9)
        gcg400.SetLineColor(9)
    if(min == 500):
        gcq500 = gamma_centralquark
        gcg500 = gamma_centralgluon
        gcq500.SetLineColor(11)
        gcg500.SetLineColor(11)
#plotting

def myText(x,y,text,color = 1):
    l = TLatex()
    l.SetTextSize(0.025)
    l.SetNDC()
    l.SetTextColor(color)
    l.DrawLatex(x,y,text)
    pass

c = TCanvas("c","c",500,500)
gcq50.Draw("HIST")
gcq50.GetXaxis().SetTitle(inputvar)
gcq50.GetYaxis().SetLabelSize(0.025)
gcq50.GetYaxis().SetTitle("Normalized Entries")

if(inputvar == "bdt"):
    gcq50.GetYaxis().SetRangeUser(0,0.1)
    gcq50.GetXaxis().SetTitle("BDT")
if(inputvar == "ntrk"):
    gcq50.GetYaxis().SetRangeUser(0,0.2)
    gcq50.GetXaxis().SetTitle("ntrk")
#gcq100.Draw("HIST same")
#gcq150.Draw("HIST same")
gcq200.Draw("HIST same")
#gcq300.Draw("HIST same")
gcq400.Draw("HIST same")
#gcq500.Draw("HIST same")

gcg50.SetLineStyle(2)
#gcg100.SetLineStyle(2)
#gcg150.SetLineStyle(2)
gcg200.SetLineStyle(2)
#gcg300.SetLineStyle(2)
gcg400.SetLineStyle(2)
#gcg500.SetLineStyle(2)
gcg50.Draw("h same")
#gcg100.Draw("h same")
#gcg150.Draw("h same")
gcg200.Draw("h same")
#gcg300.Draw("h same")
gcg400.Draw("h same")
#gcg500.Draw("h same")
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

legend.AddEntry(gcq50,"Quark","L")
legend.AddEntry(gcg50,"Gluon","L")
legend.AddEntry(gcq50,"50<p_{T}<100 GeV","F")
#legend.AddEntry(gcq100,"100<p_{T}<150 GeV","F")
#legend.AddEntry(gcq150,"150<p_{T}<200 GeV","F")
legend.AddEntry(gcq200,"200<p_{T}<300 GeV ","F")
#legend.AddEntry(gcq300,"300<p_{T}<400 GeV ","F")
legend.AddEntry(gcq400,"400<p_{T}<500 GeV ","F")
#legend.AddEntry(gcq500,"500<p_{T}<600 GeV ","F")
legend.Draw()
c.Print("./plots//gamma+/dist/gamma_"+inputvar+".pdf")


