from ROOT import *

def myText(x,y,text, color = 1):
    l = TLatex()
    l.SetTextSize(0.025)
    l.SetNDC()
    l.SetTextColor(color)
    l.DrawLatex(x,y,text)
    pass

inputvar = "ntrk"
filetype = 'dijet'
bin = [0,50,100,150,200,300,400,500,600]

dijet_sherpa = TFile( "ROOT/dijet_sherpa.root")
dijetData = TFile("ROOT/dijet_data.root")
gamma_sherpa = TFile( "ROOT/gammajet_sherpa.root")
gamaData = TFile("ROOT/gammajet_data.root")

# if filetype == 'gamma'
if inputvar == 'ntrk':
    dwpoint = [7,9,11,12,13,14,15,16]
    gwpoint = [7,8,10,11,13,14,15,16]
if inputvar == 'bdt':
    dwpoint = [32,32,32,31,31,30,30,30]
    gwpoint == [32,32,32,31,31,30,30,29]
if inputvar == 'c1':
    dwpoint = [36,35,34,33,32,32,31,30]
    gwpoint = [36,36,35,34,33,32,31,31]
if inputvar == 'width':
    dwpoint = [16,12,10,5,7,6,6,5]
    gwpoint = [15,13,10,9,8,7,7,7]

    

for i in range(0,len(bin)-1):
    min = bin[i]
    max = bin[i+1]
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

    gamma_quark = gamma_sherpa.Get(str(min)+"_LeadingJet_Central_Quark_"+inputvar)
    gamma_gluon = gamma_sherpa.Get(str(min)+"_LeadingJet_Central_Gluon_"+inputvar)

    total = dijet_quark.Clone()
    total.Add(dijet_gluon)
    total.Add(gamma_gluon)
    total.Add(gamma_quark)
  
    dijet_wp_quark = dijet_quark.Clone()
    dijet_wp_gluon= dijet_quark.Clone()
    gamma_wp_quark = dijet_quark.Clone()
    gamma_wp_gluon = dijet_quark.Clone()
    for j in range(1,dwpoint[i]+1):
        a = dijet_quark.GetBinContent(j)
        b = dijet_gluon.GetBinContent(j)
        dijet_wp_quark.SetBinContent(j,a+b)
        dijet_wp_gluon.SetBinContent(j,0)
    for j in range(1,gwpoint[i]+1):
        a = gamma_quark.GetBinContent(j)
        b = gamma_gluon.GetBinContent(j)
        gamma_wp_quark.SetBinContent(j,a+b)
        gamma_wp_gluon.SetBinContent(j,0)
    for j in range(dwpoint[i]+1,dijet_quark.GetNbinsX()+1):
        a = dijet_quark.GetBinContent(j)
        b = dijet_gluon.GetBinContent(j)
        dijet_wp_quark.SetBinContent(j,0)
        dijet_wp_gluon.SetBinContent(j,a+b)
    for j in range(gwpoint[i]+1,gamma_quark.GetNbinsX()+1):
        a = gamma_quark.GetBinContent(j)
        b = gamma_gluon.GetBinContent(j)
        gamma_wp_quark.SetBinContent(j,0)
        gamma_wp_gluon.SetBinContent(j,a+b)
    c = TCanvas("","",300,300)
    gStyle.SetOptStat(0)
    dijet_wp_quark.GetYaxis().SetRangeUser(-0.0000001,total.GetMaximum()*1.2)
    dijet_wp_quark.GetYaxis().SetLabelSize(0.02)
    dijet_wp_quark.GetYaxis().SetTitle("events")

    dijet_wp_quark.SetLineColor(1)
    gamma_wp_quark.SetLineColor(8)
    dijet_wp_gluon.SetLineColor(2)
    gamma_wp_gluon.SetLineColor(4)


    if(inputvar == 'bdt' or inputvar == 'c1'):
        if(inputvar == 'bdt'):
            dijet_wp_quark.GetXaxis().SetTitle('BDT')
        if(inputvar == 'c1'):
            dijet_wp_quark.GetXaxis().SetTitle('c1')
        leg = TLegend(0.14,0.5,0.45,0.72)
        leg.SetFillColor(0)
        leg.SetBorderSize(0)
        leg.SetFillStyle(0)
        leg.AddEntry(dijet_wp_quark,"dijet quark",'l')
        leg.AddEntry(dijet_wp_gluon,"dijetgluon",'l')
        leg.AddEntry(gamma_wp_quark,"gamma quark",'l')
        leg.AddEntry(gamma_wp_gluon,"gamma gluon",'l')
    if(inputvar =='ntrk' or inputvar =='width'):
        if(inputvar == 'ntrk'):
            dijet_wp_quark.GetXaxis().SetTitle('ntrk')
        if(inputvar == 'width'):
            dijet_wp_quark.GetXaxis().SetTitle('width')
        leg = TLegend(0.5,0.5,0.85,0.72)
        leg.SetFillColor(0)
        leg.SetBorderSize(0)
        leg.SetFillStyle(0)
        leg.AddEntry(dijet_wp_quark,"dijet quark",'l')
        leg.AddEntry(dijet_wp_gluon,"dijetgluon",'l')
        leg.AddEntry(gamma_wp_quark,"gamma quark",'l')
        leg.AddEntry(gamma_wp_gluon,"gamma gluon",'l')
    dijet_wp_quark.Draw("hist")
    gamma_wp_quark.Draw("hist same")
    gamma_wp_gluon.Draw("hist same")
    dijet_wp_gluon.Draw("hist same")
    leg.Draw('same')
    
    myText(0.18,0.84,"#it{#bf{#scale[1.8]{#bf{ATLAS} Simulation Internal}}}")
    myText(0.18,0.80,"#bf{#scale[1.5]{#sqrt{s} = 13 TeV}}")
    myText(0.18,0.76,'#bf{#scale[1.3]{'+str(min)+' < p_{T} < '+str(max)+' GeV}}')

    c.Print("./WP/wp_" +inputvar+"_"+str(min)+".pdf")
