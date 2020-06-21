from ROOT import *
import numpy as np

def myText(x,y,text,color=1):
    l = TLatex()
    l.SetTextSize(0.025)
    l.SetNDC()
    l.SetTextColor(color)
    l.DrawLatex(x,y,text)
    pass

var = "ntrk"
file0 = TFile("ROOT/gammajet_sherpa.root")
file1 = TFile("ROOT/dijet_sherpa_py_forGamma40_2000.root")

file3 = TFile("ROOT/dijet_sherpa_py_forGamma40_500_eta.root")
file4 = TFile("ROOT/gammajet_dijet_sherpa_eta_40_500_fix.root")

bin =np.array( [0,50,100,150,200,300,400,500,600,700])
bin2 = [0.0,0.5,1,2.1]

gStyle.SetOptStat(0)

c = TCanvas("","",500,500)
c.SetGrid()
gPad.SetTickx()
gPad.SetTicky()

pt_higher_quark =  TH1F("pt_higher_quark","",7,0,500)
pt_higher_gluon =  TH1F("pt_higher_gluon","",7,0,500)
pt_lower_quark = TH1F("pt_lower_quark","",7,0,500)
pt_lower_gluon = TH1F("pt_lower_gluon","",7,0,500)

eta_higher_quark = TH1F("eta_higher_quark","",3,np.asarray(bin2))
eta_higher_gluon = TH1F("eta_higher_gluon","",3,np.asarray(bin2))
eta_lower_quark = TH1F("eta_lower","",3,np.asarray(bin2))
eta_lower_gluon = TH1F("eta_lower_gluon","",3,np.asarray(bin2))


fq1_list = np.zeros(6) #these will hold fq values for different pt ranges
fq2_list = np.zeros(6)

for i in range(0,7):
    lower_quark0 = file1.Get(str(bin[i]) + "_LeadingJet_Forward_Quark_" + var)
    lower_gluon0 = file1.Get(str(bin[i]) + "_LeadingJet_Forward_Gluon_" + var)

    lower1_quark=  file1.Get(str(bin[i]) + "_LeadingJet_Central_Quark_" + var)
    lower1_gluon = file1.Get(str(bin[i]) + "_LeadingJet_Central_Gluon_" + var)

    lower_quark = file1.Get(str(bin[i])+"_SubJet_Forward_Quark_"+var)
    lower_gluon = file1.Get(str(bin[i])+"_SubJet_Forward_Gluon_"+var)


    lower_quark1 = file1.Get(str(bin[i])+"_SubJet_Central_Quark_"+var)
    lower_gluon1 = file1.Get(str(bin[i])+"_SubJet_Central_Gluon_"+var)
    for a in range(60):
        if np.isnan(lower_quark.GetBinContent(a)):
            lower_quark.SetBinContent(a,0)
        if np.isnan(lower_gluon.GetBinContent(a)):
            lower_gluon.SetBinContent(a,0)
        if np.isnan(lower_quark1.GetBinContent(a)):
            lower_quark1.SetBinContent(a,0)
        if np.isnan(lower_gluon1.GetBinContent(a)):
            lower_gluon1.SetBinContent(a,0)
        if np.isnan(lower_quark0.GetBinContent(a)):
            lower_quark0.SetBinContent(a,0)
        if np.isnan(lower_gluon0.GetBinContent(a)):
            lower_gluon0.SetBinContent(a,0)
        if np.isnan(lower1_quark.GetBinContent(a)):
            lower1_quark.SetBinContent(a,0)
        if np.isnan(lower1_gluon.GetBinContent(a)):
            lower1_gluon.SetBinContent(a,0)




    lower_quark.Add(lower_quark1)
    lower_gluon.Add(lower_gluon1)
    lower_quark0.Add(lower1_quark)
    lower_gluon0.Add(lower1_gluon)
    lower_quark.Add(lower_quark0)
    lower_gluon.Add(lower_gluon0)
    higher_quark = file0.Get(str(bin[i])+"_LeadingJet_Central_Quark_"+var)

    higher_gluon = file0.Get(str(bin[i])+"_LeadingJet_Central_Gluon_"+var)


    tq1 = 0.  #1 refers to higher eta jet, 2 refers to lower eta
    tg1 = 0.
    tq2 = 0.
    tg2 = 0.

    var_q1 = 0.
    var_q2 = 0.
    var_g1 = 0.
    var_g2 = 0.

    for j in range(1, higher_quark.GetNbinsX()+1):
        tq1 += higher_quark.GetBinContent(j)
        tg1 += higher_gluon.GetBinContent(j)
        tq2 += lower_quark.GetBinContent(j)
        tg2 += lower_gluon.GetBinContent(j)

#        var_q1 += (higher_quark.GetBinError(j)*higher_quark.GetBinError(j))
#        var_q2 += (lower_quark.GetBinError(j)*lower_quark.GetBinError(j))
#        var_g1 += (higher_gluon.GetBinError(j)*higher_gluon.GetBinError(j))
#        var_g1 += (lower_gluon.GetBinError(j)*lower_gluon.GetBinError(j))

#    var_tot_1 = var_q1 + var_g1
#    var_tot_2 = var_q2 + var_g2

    fq1 = tq1/(tq1+tg1)
    fq2 = tq2/(tq2+tg2)
    fg1 = 1.-fq1
    fg2 = 1.-fq2



    #print(fg2)
#    var_fq1 = fq1*fq1 * ((var_tot_1 / ((tq1+tg1)*(tq1+tg1))) + (var_q1/(tq1*tq1)))
#    var_fq2 = fq2*fq2 * ((var_tot_2 / ((tq2+tg2)*(tq2+tg2))) + (var_q2/(tq2*tq2)))
#    var_fg1 = fg1*fg1 * ((var_tot_1 / ((tq1+tg1)*(tq1+tg1))) + (var_q1/(tq1*tq1)))
#    var_fg2 = fg2*fg2 * ((var_tot_2 / ((tq2+tg2)*(tq2+tg2))) + (var_q2/(tq2*tq2)))

    pt_higher_quark.SetBinContent(i+1,fq1)
    pt_higher_gluon.SetBinContent(i+1,fg1)
    pt_lower_quark.SetBinContent(i+1,fq2)
    pt_lower_gluon.SetBinContent(i+1,fg2)

   # pt_higher_quark.SetBinError(i+1,np.sqrt(var_fq1))
   # pt_higher_gluon.SetBinError(i+1,np.sqrt(var_fg1))
   # pt_lower_quark.SetBinError(i+1,np.sqrt(var_fq2))
   # pt_lower_gluon.SetBinError(i+1,np.sqrt(var_fg2))

pt_higher_quark.SetMaximum(1.)
pt_higher_quark.SetMinimum(0.)
pt_higher_quark.GetYaxis().SetTitle("Fraction")
pt_higher_quark.GetXaxis().SetTitle("p_{T}[GeV]")
pt_higher_quark.SetLineWidth(6)
pt_higher_gluon.SetLineWidth(6)
pt_lower_quark.SetLineWidth(6)
pt_lower_gluon.SetLineWidth(6)

pt_higher_gluon.SetLineColor(2)
pt_lower_quark.SetLineColor(3)
pt_lower_gluon.SetLineColor(6)

leg1 = TLegend(.15,0.15,0.45,0.3)
leg1.AddEntry(pt_higher_quark,"f_{Gamma+jet,Q}","l")
leg1.AddEntry(pt_higher_gluon,"f_{Gamma+jet,G}","l")
leg1.AddEntry(pt_lower_quark,"f_{Multi-jet,Q}","l")
leg1.AddEntry(pt_lower_gluon,"f_{Multi-jet,G}","l")
leg1.SetBorderSize(0)
leg1.SetFillStyle(0)

pt_higher_quark.Draw("HIST ")
pt_higher_gluon.Draw("HIST  same")
pt_lower_quark.Draw("HIST  same")
pt_lower_gluon.Draw("HIST  same")
leg1.Draw("same")

myText(0.14,0.84,'#it{#bf{#scale[1.4]{#bf{ATLAS} Simulation Preliminary}}}')
#myText(0.14,0.80,'#bf{#scale[1.2]{#sqrt{s}=13 TeV}}')
#myText(0.14,0.76,'#bf{#scale[1.2]{Anti-K_{t} EM+JES R=0.4}}')

c.Print("./plots/fraction_plots/pt-fraction_"+var+".pdf")

for i in range(0,2):
    lower_quark0_eta = file3.Get(str(bin2[i]) + "_LeadingJet_Forward_Quark_" + var)
    lower_gluon0_eta = file3.Get(str(bin2[i]) + "_LeadingJet_Forward_Gluon_" + var)
    lower1_quark_eta =  file3.Get(str(bin2[i]) + "_LeadingJet_Central_Quark_" + var)
    lower1_gluon_eta = file3.Get(str(bin2[i]) + "_LeadingJet_Central_Gluon_" + var)


    lower_quark_eta = file3.Get(str(bin2[i])+"_SubJet_Forward_Quark_"+var)
    lower_gluon_eta = file3.Get(str(bin2[i])+"_SubJet_Forward_Gluon_"+var)

    lower_quark1_eta = file3.Get(str(bin2[i])+"_SubJet_Central_Quark_"+var)
    lower_gluon1_eta = file3.Get(str(bin2[i])+"_SubJet_Central_Gluon_"+var)

    #print(type(bin2[2]))
    #print(bin2[i])

    for a in range(0,60):
        if np.isnan(lower_quark_eta.GetBinContent(a)):
            lower_quark_eta.SetBinContent(a,0)
        if np.isnan(lower_gluon_eta.GetBinContent(a)):
            lower_gluon_eta.SetBinContent(a,0)
        if np.isnan(lower_quark1_eta.GetBinContent(a)):
            lower_quark1_eta.SetBinContent(a,0)
        if np.isnan(lower_gluon1_eta.GetBinContent(a)):
            lower_gluon1_eta.SetBinContent(a,0)
        if np.isnan(lower_quark0_eta.GetBinContent(a)):
            lower_quark0_eta.SetBinContent(a,0)
        if np.isnan(lower_gluon0_eta.GetBinContent(a)):
            lower_gluon0_eta.SetBinContent(a,0)
        if np.isnan(lower1_quark_eta.GetBinContent(a)):
            lower1_quark_eta.SetBinContent(a,0)
        if np.isnan(lower1_gluon_eta.GetBinContent(a)):
            lower1_gluon_eta.SetBinContent(a,0)


    lower_quark_eta.Add(lower_quark1_eta)
    lower_gluon_eta.Add(lower_gluon1_eta)
    lower_quark0_eta.Add(lower1_quark_eta)
    lower_gluon0_eta.Add(lower1_gluon_eta)
    lower_quark_eta.Add(lower_quark0_eta)
    lower_gluon_eta.Add(lower_gluon0_eta)





    higher_quark_eta = file4.Get(str(bin2[i])+"_LeadingJet_Central_Quark_"+var)

    higher_gluon_eta = file4.Get(str(bin2[i])+"_LeadingJet_Central_Gluon_"+var)

    tq1 = 0. #1 refers to higher eta jet, 2 refers to lower eta
    tg1 = 0.
    tq2 = 0.
    tg2 = 0.



    for j in range(1, higher_quark_eta.GetNbinsX()+1):
        tq1 += higher_quark_eta.GetBinContent(j)
        tg1 += higher_gluon_eta.GetBinContent(j)
        tq2 += lower_quark_eta.GetBinContent(j)
        tg2 += lower_gluon_eta.GetBinContent(j)

    fq1 = tq1/(tq1+tg1)
    fq2 = tq2/(tq2+tg2)
    fg1 = 1.-fq1
    fg2 = 1.-fq2

    eta_higher_quark.SetBinContent(i+1,fq1)
    eta_higher_gluon.SetBinContent(i+1,fg1)
    eta_lower_quark.SetBinContent(i+1,fq2)
    eta_lower_gluon.SetBinContent(i+1,fg2)

eta_higher_quark.SetMaximum(1.)
eta_higher_quark.SetMinimum(0.)
eta_higher_quark.GetYaxis().SetTitle("Fraction")
eta_higher_quark.GetXaxis().SetTitle("|\eta|")
eta_higher_quark.SetLineWidth(6)
eta_higher_gluon.SetLineWidth(6)
eta_lower_quark.SetLineWidth(6)
eta_lower_gluon.SetLineWidth(6)

eta_higher_gluon.SetLineColor(2)
eta_lower_quark.SetLineColor(3)
eta_lower_gluon.SetLineColor(6)

leg1 = TLegend(.15,0.15,0.45,0.3)
leg1.AddEntry(pt_higher_quark,"f_{Gamma+jet,Q}","l")
leg1.AddEntry(pt_higher_gluon,"f_{Gamma+jet,G}","l")
leg1.AddEntry(pt_lower_quark,"f_{Multi-jet,Q}","l")
leg1.AddEntry(pt_lower_gluon,"f_{Multi-jet,G}","l")
leg1.SetBorderSize(0)
leg1.SetFillStyle(0)

eta_higher_quark.Draw("HIST ")
eta_higher_gluon.Draw("HIST  same")
eta_lower_quark.Draw("HIST  same")
eta_lower_gluon.Draw("HIST  same")
leg1.Draw("same")

myText(0.14,0.84,'#it{#bf{#scale[1.4]{#bf{ATLAS} Simulation Preliminary}}}')
#

c.Print("./plots/fraction_plots/eta-fraction.pdf")
