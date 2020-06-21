from ROOT import *
bins = [0, 50, 100, 150, 200, 300, 400, 500, 600, 800, 1000, 1200, 1500, 2000]
HistMap = {}
JetList = []


c = TCanvas("c","c",500,500)
h2 = TH1F("","",150,0,2000)
#fileinput = TFile.Open("gammajet_sherpa_incl.root")
fileinput = TFile.Open("/eos/user/h/hmyin/gammajet_pythia/gammajet_pythia_incl.root")
t1 = fileinput.Get("tree_photon")

for i in t1:
		if i.jet_pt[0]/1000 > 40 and i.jet_pt[0]/1000 < 2000 and abs(i.jet_eta[0]) < 2.1 :
				i.jet_pt[0] = i.jet_pt[0]/1000

				weight_all = i.syst_weight_xsec #i.pdfWeights[0] is nominal
                h2.Fill(i.jet_pt[0],weight_all)
gStyle.SetOptStat(0)
gPad.SetLogy()



h2.Draw("HIST")
h2.GetXaxis().SetTitle("p_{t} (GeV)")
l = TLatex()
l.SetTextSize(0.025)
l.SetNDC()
l.SetTextColor(1)
l.DrawLatex(0.15,0.84,"#it{#bf{#scale[1.8]{#bf{ATLAS} Simulation Preliminary}}}");
l.DrawLatex(0.15,0.80,"#bf{#scale[1.5]{#sqrt{s} = 13 TeV}}");
l.DrawLatex(0.15,0.76,"#bf{#scale[1.5]{Leading Jet P_{t} Spectrum, Sherpa}}");

c.Print("pt-spec_gamma-pythia.png")
