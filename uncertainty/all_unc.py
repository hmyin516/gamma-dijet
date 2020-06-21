import numpy as np
from ROOT import *

doreweight = 0
inputvar = "bdt"
var = inputvar
def myText(x,y,text,color =1):
    l = TLatex()
    l.SetTextSize(0.025)
    l.SetNDC()
    l.SetTextColor(color)
    l.DrawLatex(x,y,text)
    pass


dijetsherpa = TFile("ROOT/dijet_sherpa_py_forGamma_full.root")
ntrackall3  = TFile("ROOT/dijet_data_py_forGamma.root")
gammasherpa = TFile("ROOT/gammajet_sherpa.root")
gammadata = TFile("ROOT/gammajet_data.root")
dijetpythia = TFile("ROOT/dijet_pythia_fixed.root")
gammapythia = TFile("ROOT/gammajet_pythia.root")


bin = [0,50,100,150,200,300,400,500,600,800,1000,1200,1500,2000]
for i in range(1,7):   #for only dijet event, start from jet pT>500 GeV
#for i in range(13):	#for gamma+jet combined with dijet event, start from jet pT>0 GeV
    min = bin[i]
    max = bin[i+1]

    #sherpa
    dijet_quark = dijetsherpa.Get(str(min)+"_LeadingJet_Forward_Quark_"+inputvar)
    dijet_subjetquark = dijetsherpa.Get(str(min)+"_SubJet_Forward_Quark_"+inputvar)
    dijet_gluon = dijetsherpa.Get(str(min)+"_LeadingJet_Forward_Gluon_"+inputvar)
    dijet_subjetgluon = dijetsherpa.Get(str(min)+"_SubJet_Forward_Gluon_"+inputvar)
    dijet_quark2 = dijetsherpa.Get(str(min)+"_LeadingJet_Central_Quark_"+inputvar)
    dijet_subjetquark2 = dijetsherpa.Get(str(min)+"_SubJet_Central_Quark_"+inputvar)
    dijet_gluon2 = dijetsherpa.Get(str(min)+"_LeadingJet_Central_Gluon_"+inputvar)
    dijet_subjetgluon2 = dijetsherpa.Get(str(min)+"_SubJet_Central_Gluon_"+inputvar)
    gamma_quark = gammasherpa.Get(str(min) + "_LeadingJet_Central_Quark_" + inputvar)
    gamma_gluon = gammasherpa.Get(str(min) + "_LeadingJet_Central_Gluon_" + inputvar)
    #pythia
    dijet_quark_pythia = dijetpythia.Get(str(min)+"_LeadingJet_Forward_Quark_"+inputvar)
    dijet_subjetquark_pythia = dijetpythia.Get(str(min)+"_SubJet_Forward_Quark_"+inputvar)
    dijet_gluon_pythia = dijetpythia.Get(str(min)+"_LeadingJet_Forward_Gluon_"+inputvar)
    dijet_subjetgluon_pythia = dijetpythia.Get(str(min)+"_SubJet_Forward_Gluon_"+inputvar)
    dijet_quark2_pythia = dijetpythia.Get(str(min)+"_LeadingJet_Central_Quark_"+inputvar)
    dijet_subjetquark2_pythia = dijetpythia.Get(str(min)+"_SubJet_Central_Quark_"+inputvar)
    dijet_gluon2_pythia = dijetpythia.Get(str(min)+"_LeadingJet_Central_Gluon_"+inputvar)
    dijet_subjetgluon2_pythia = dijetpythia.Get(str(min)+"_SubJet_Central_Gluon_"+inputvar)

    gamma_quark_pythia = gammapythia.Get(str(min) + "_LeadingJet_Central_Quark_" + inputvar)
    gamma_gluon_pythia = gammapythia.Get(str(min) + "_LeadingJet_Central_Gluon_" + inputvar)
    #data
    dijet_data1 = ntrackall3.Get(str(min)+"_LeadingJet_Forward_Data_"+inputvar)
    dijet_data2 = ntrackall3.Get(str(min)+"_LeadingJet_Central_Data_"+inputvar)

    dijet_data3 = ntrackall3.Get(str(min)+"_SubJet_Forward_Data_" + inputvar)
    dijet_data4 = ntrackall3.Get(str(min)+"_SubJet_Central_Data_" + inputvar)

    gamma_data = gammadata.Get(str(min)+"_LeadingJet_Central_Data_"+inputvar)

    dijet_subjetquark.Add(dijet_subjetquark2)
    dijet_subjetgluon.Add(dijet_subjetgluon2)
    dijet_quark.Add(dijet_quark2)
    dijet_gluon.Add(dijet_gluon2)
    dijet_quark.Add(dijet_subjetquark)
    dijet_gluon.Add(dijet_subjetgluon)

    dijet_data1.Add(dijet_data2)
    dijet_data3.Add(dijet_data4)
    dijet_data1.Add(dijet_data3)

    dijet_subjetquark_pythia.Add(dijet_subjetquark2_pythia)
    dijet_subjetgluon_pythia.Add(dijet_subjetgluon2_pythia)
    dijet_quark_pythia.Add(dijet_quark2_pythia)
    dijet_gluon_pythia.Add(dijet_gluon2_pythia)
    dijet_quark_pythia.Add(dijet_subjetquark_pythia)
    dijet_gluon_pythia.Add(dijet_subjetgluon_pythia)

    #reassigning to variables
    higher_quark = gamma_quark
    higher_gluon = gamma_gluon
    lower_quark = dijet_quark
    lower_gluon = dijet_gluon

    higher_data = gamma_data
    lower_data = dijet_data1

    higher_quark_pythia = gamma_quark_pythia
    higher_gluon_pythia = gamma_gluon_pythia
    lower_quark_pythia = dijet_quark_pythia
    lower_gluon_pythia = dijet_gluon_pythia

    ToT_Fq2 = 0.
    ToT_Fg2 = 0.
    ToT_Cq2 =0.
    ToT_Cg2 = 0.

    ToT_Fq2_pythia = 0.
    ToT_Fg2_pythia = 0.
    ToT_Cq2_pythia =0.
    ToT_Cg2_pythia = 0.

    for j in range(1,lower_quark.GetNbinsX()+1):
		ToT_Fq2+=higher_quark.GetBinContent(j)  #dijetquark
		ToT_Cq2+=lower_quark.GetBinContent(j) #gammaquark
		ToT_Fg2+=higher_gluon.GetBinContent(j) #dijetlguon
		ToT_Cg2+=lower_gluon.GetBinContent(j)#gammagluon

		ToT_Fq2_pythia+=higher_quark_pythia.GetBinContent(j)  #dijetquark
		ToT_Cq2_pythia+=lower_quark_pythia.GetBinContent(j) #gammaquark
		ToT_Fg2_pythia+=higher_gluon_pythia.GetBinContent(j) #dijetlguon
		ToT_Cg2_pythia+=lower_gluon_pythia.GetBinContent(j)#gammagluon
    if ((ToT_Fg2+ToT_Fq2) != 0):
		fg=ToT_Fg2/(ToT_Fg2+ToT_Fq2)
		cg=ToT_Cg2/(ToT_Cq2+ToT_Cg2)
		fg_pythia = ToT_Fg2_pythia/(ToT_Fg2_pythia + ToT_Fq2_pythia)
		cg_pythia = ToT_Cg2_pythia/(ToT_Cq2_pythia + ToT_Cg2_pythia)
    else:
		continue

    fq=1.-fg
    cq=1.-cg
    fq_pythia = 1.-fg_pythia
    cq_pythia = 1.-cg_pythia

    if (doreweight):
        for i in range(1,higher_quark.GetNbinsX()+1):
            if (lower_quark.GetBinContent(i) > 0 and lower_gluon.GetBinContent(i) > 0):
                #print i,higher_quark.GetBinContent(i)/lower_quark.GetBinContent(i),higher_gluon.GetBinContent(i)/lower_gluon.GetBinContent(i)
                factor_gluon = higher_gluon.GetBinContent(i)/lower_gluon.GetBinContent(i)
                factor_quark = higher_quark.GetBinContent(i)/lower_quark.GetBinContent(i)
                lower_quark.SetBinContent(i,lower_quark.GetBinContent(i)*factor_quark)
                lower_gluon.SetBinContent(i,lower_gluon.GetBinContent(i)*factor_quark)
                lower_data.SetBinContent(i,lower_data.GetBinContent(i)*factor_quark)
                pass
            pass
        pass
    unscaled_higher = higher_data.Clone("")
    unscaled_lower = lower_data.Clone("")
    if(lower_quark.Integral() != 0):
		lower_quark.Scale(1./lower_quark.Integral())
    if(lower_gluon.Integral() != 0):
		lower_gluon.Scale(1./lower_gluon.Integral())
    if(higher_quark.Integral() != 0):
		higher_quark.Scale(1./higher_quark.Integral())
    if(higher_gluon.Integral() != 0):
		higher_gluon.Scale(1./higher_gluon.Integral())
    if(lower_quark_pythia.Integral() != 0):
		lower_quark_pythia.Scale(1./lower_quark_pythia.Integral())
    if(lower_gluon_pythia.Integral() != 0):
		lower_gluon_pythia.Scale(1./lower_gluon_pythia.Integral())
    if(higher_quark_pythia.Integral() != 0):
		higher_quark_pythia.Scale(1./higher_quark_pythia.Integral())
    if(higher_gluon_pythia.Integral() != 0):
		higher_gluon_pythia.Scale(1./higher_gluon_pythia.Integral())
    if(lower_data.Integral() != 0):
        lower_data.Scale(1./lower_data.Integral())
    if(higher_data.Integral() != 0):
        higher_data.Scale(1./higher_data.Integral())

    higher = higher_quark.Clone("")
    lower = higher_quark.Clone("")
    higher_pythia = higher_quark_pythia.Clone("")
    lower_pythia = higher_quark_pythia.Clone("")

    #sherpa
    for i in range(1,higher.GetNbinsX()+1):
        higher.SetBinContent(i,fg*higher_gluon.GetBinContent(i)+fq*higher_quark.GetBinContent(i))
        lower.SetBinContent(i,cg*lower_gluon.GetBinContent(i)+cq*lower_quark.GetBinContent(i))

        higher_pythia.SetBinContent(i,fg_pythia*higher_gluon_pythia.GetBinContent(i)+fq_pythia*higher_quark_pythia.GetBinContent(i))
        lower_pythia.SetBinContent(i,cg_pythia*lower_gluon_pythia.GetBinContent(i)+cq_pythia*lower_quark_pythia.GetBinContent(i))

        pass

    quark = higher_quark.Clone("")
    gluon = higher_quark.Clone("")
    quark_pythia = higher_quark_pythia.Clone("")
    gluon_pythia = higher_quark_pythia.Clone("")
    quark_data = higher_data.Clone("")
    gluon_data = higher_data.Clone("")
    #sherpa
    for i in range(1,higher.GetNbinsX()+1):
        F = higher.GetBinContent(i)
        C = lower.GetBinContent(i)
        if((cg*fq-fg*cq) != 0 ):
            Q = -(C*fg-F*cg)/(cg*fq-fg*cq)
            G = (C*fq-F*cq)/(cg*fq-fg*cq)
            quark.SetBinContent(i,Q)
            gluon.SetBinContent(i,G)
            #print "   ",i,G,higher_gluon.GetBinContent(i),lower_gluon.GetBinContent(i)
        pass

    #pythia
    for i in range(1,higher_pythia.GetNbinsX()+1):
        F = higher_pythia.GetBinContent(i)
        C = lower_pythia.GetBinContent(i)
        if((cg_pythia*fq_pythia-fg_pythia*cq_pythia) != 0):
            Q = -(C*fg_pythia-F*cg_pythia)/(cg_pythia*fq_pythia-fg_pythia*cq_pythia)
            G = (C*fq_pythia-F*cq_pythia)/(cg_pythia*fq_pythia-fg_pythia*cq_pythia)
            quark_pythia.SetBinContent(i,Q)
            gluon_pythia.SetBinContent(i,G)
    #data
    for i in range(1,higher_data.GetNbinsX()+1):
        F = higher_data.GetBinContent(i)
        C = lower_data.GetBinContent(i)
        if((cg*fq-fg*cq) != 0):
            Q = -(C*fg-F*cg)/(cg*fq-fg*cq)
            G = (C*fq-F*cq)/(cg*fq-fg*cq)
            quark_data.SetBinContent(i,Q)
            gluon_data.SetBinContent(i,G)
            #print "   ",i,"  ",G,"   ",Q
        pass
    tot_unc_q = []
    tot_unc_g = []

    for j in range(0,quark.GetNbinsX()):
        tot_unc_q += [np.zeros(3)]
        tot_unc_g += [np.zeros(3)]

    #stat_mc
    nstraps = 5000
    Qvals = []
    Gvals = []
    for j in range (1,higher_data.GetNbinsX()+1):
        Qvals += [np.zeros(nstraps)]
        Gvals += [np.zeros(nstraps)]
    for k in range(nstraps):
        forward_data_strap = higher_data.Clone("f"+str(k))
        central_data_strap = lower_data.Clone("c"+str(k))
        #print(higher_data.GetBinContent(j))
        for j in range(1,higher.GetNbinsX()+1):
            hp = np.random.poisson(unscaled_higher.GetBinContent(j))
            lp = np.random.poisson(unscaled_lower.GetBinContent(j))
            #print(hp)
            forward_data_strap.SetBinContent(j,hp)
            central_data_strap.SetBinContent(j,lp)
        if (forward_data_strap.Integral() != 0):
            forward_data_strap.Scale(1./forward_data_strap.Integral())
        if(central_data_strap.Integral() != 0):
            central_data_strap.Scale(1./central_data_strap.Integral())
        #for a in range(0,higher.GetNbinsX()):
            #print(central_data_strap.GetBinContent(a))

        for j in range(0,higher_data.GetNbinsX()):
            F_strap = forward_data_strap.GetBinContent(j)
            C_strap = central_data_strap.GetBinContent(j)
            Q_strap = -(C_strap*fg-F_strap*cg)/(cg*fq-fg*cq)
            G_strap = (C_strap*fq- F_strap*cq)/(cg*fq-fg*cq)

            Qvals[j][k] = Q_strap
            Gvals[j][k] = G_strap

    quark_strap = higher_data.Clone("")
    gluon_strap = higher_data.Clone("")


    ####
    # This checks to see if original data is similar to poisson generated data
    #forward_data_strap.Draw("HIST")
    #forward_data_strap.GetYaxis().SetRangeUser(0,1)
    #gStyle.SetOptStat(0)
    #myText(0.58,0.82,"#bf{#scale[1.5]{pT range: forward_data_strap"+str(min)+" - "+str(max)+" GeV}}")
    #forward_data_strap.GetYaxis().SetRangeUser(0,1)
    #forward_data_strap.SetLineColor(2)
    #c.Print("./plots/gamma+/stat/plots_" + var + "/" + str(min) + "forward_strap.png")
    #plotting.Draw("HIST ")
    #myText(0.58,0.82,"#bf{#scale[1.5]{pT range: data"+str(min)+" - "+str(max)+" GeV}}")
    #plotting.GetYaxis().SetRangeUser(0,1)
    #.Print("./plots/gamma+/stat/plots_" + var + "/" + str(min) + "data.png")
    ####
    for j in range(0,higher_data.GetNbinsX()):
        Qvals[j].sort()
        Gvals[j].sort()
        Q = np.median(Qvals[j])
        #print(Q)
        G = np.median(Gvals[j])
        sigmaQ = .5*(Qvals[j][int(.84*len(Qvals[j]))] - Qvals[j][int(.16*len(Qvals[j]))])

        sigmaG = .5*(Gvals[j][int(.84*len(Gvals[j]))] - Gvals[j][int(.16*len(Gvals[j]))])
        if(Q != 0):
            sigmaQ = np.abs(sigmaQ/Q)
            #print(sigmaQ)
        if(G != 0):
            sigmaG = np.abs(sigmaG/G)

        tot_unc_q[j][0] = sigmaQ
        tot_unc_g[j][0] = sigmaG

        quark_strap.SetBinContent(j,sigmaQ)
        gluon_strap.SetBinContent(j,sigmaG)
    quark_strap.Scale(100)
    gluon_strap.Scale(100)

    quark_negative = quark_strap.Clone("") * -1
    gluon_negative = gluon_strap.Clone("") * -1

    #MC
    quark_copy = quark.Clone("")
    gluon_copy = gluon.Clone("")

    quarkMC_negative = quark.Clone()
    gluonMC_negative = gluon.Clone()

    quark_copy.Add(higher_quark)
    gluon_copy.Add(higher_gluon)


    quark_use = quark.Clone("")
    gluon_use = gluon.Clone("")

    quark_use.Add(higher_quark,-1)
    gluon_use.Add(higher_gluon,-1)

    for j in range(1,quark.GetNbinsX()+1):
        a = quark_use.GetBinContent(j)
        b = gluon_use.GetBinContent(j)

        a = np.absolute(a)
        b = np.absolute(b)
        tot_unc_q[j-1][1] = a
        tot_unc_g[j-1][1] = b
        quark_use.SetBinContent(j,a)
        gluon_use.SetBinContent(j,b)

        quarkMC_negative.SetBinContent(j,-1*a)
        gluonMC_negative.SetBinContent(j,-1*b)

    quark_use.Divide(quark_copy)
    gluon_use.Divide(gluon_copy)

    quarkMC_negative.Divide(quark_copy)
    gluonMC_negative.Divide(gluon_copy)

    for j in range(0,quark.GetNbinsX()):
        tot_unc_q[j][1] = quark_use.GetBinContent(j+1)
        tot_unc_g[j][1] = gluon_use.GetBinContent(j+1)
     #showering uncertianty
    quark_show_copy = quark.Clone("")
    gluon_show_copy = gluon.Clone("")

    quark_show_use = quark.Clone("")
    gluon_show_use = gluon.Clone("")

    quark_show_negative = quark.Clone("")
    gluon_show_negative = quark.Clone("")

    quark_show_copy.Add(quark_pythia)
    gluon_show_copy.Add(gluon_pythia)

    quark_show_copy.Scale(0.5)
    gluon_show_copy.Scale(0.5)

    quark_show_use.Add(quark_pythia,-1)
    gluon_show_use.Add(gluon_pythia,-1)

    for j in range(1,quark.GetNbinsX()+1):
        c = quark_show_use.GetBinContent(j)
        d = gluon_show_use.GetBinContent(j)

        c = np.absolute(c)
        d = np.absolute(d)

        quark_show_use.SetBinContent(j,a)
        gluon_show_use.SetBinContent(j,b)

        quark_show_negative.SetBinContent(j,-1*a)
        gluon_show_negative.SetBinContent(j,-1*b)

    quark_show_use.Divide(quark_show_copy)
    gluon_show_use.Divide(gluon_show_copy)

    quark_show_negative.Divide(quark_show_copy)
    gluon_show_negative.Divide(gluon_show_copy)

    for j in range(0,quark.GetNbinsX()):
        tot_unc_q[j][2] = quark_show_use.GetBinContent(j+1)
        tot_unc_g[j][2] = gluon_show_use.GetBinContent(j+1)

    #total
    q_sigma_total = quark.Clone("")
    g_sigma_total = gluon.Clone("")

    for j in range(0, quark.GetNbinsX()):
        a = tot_unc_q[j][0]
        b = tot_unc_q[j][1]
        c = tot_unc_q[j][2]
        q_sigma_tot = np.sqrt((a**2)+(b**2)+(c**2))

        a = tot_unc_g[j][0]
        b = tot_unc_g[j][1]
        c = tot_unc_g[j][2]
        g_sigma_tot = np.sqrt((a**2)+(b**2)+(c**2))
        q_sigma_total.SetBinContent(j+1,q_sigma_tot)
        g_sigma_total.SetBinContent(j+1,g_sigma_tot)
    q_sigma_total.Scale(100)
    g_sigma_total.Scale(100)



    neg_q_sigma_tot =  q_sigma_total.Clone("") * -1
    neg_g_sigma_tot =  g_sigma_total.Clone("") * -1
    #showering
    quark_show_use.Scale(100)
    gluon_show_use.Scale(100)
    quark_show_negative.Scale(100)
    gluon_show_negative.Scale(100)
    #mc
    quark_use.Scale(100)
    gluon_use.Scale(100)
    quarkMC_negative.Scale(100)
    gluonMC_negative.Scale(100)
    #stat
    #quark_strap.Scale(100)
    ##gluon_strap.Scale(100)
    #quark_negative.Scale(100)
    #gluon_negative.Scale(100)

    c = TCanvas("c","c",500,500)
    gPad.SetLeftMargin(0.15)
    gPad.SetTopMargin(0.05)
    gPad.SetBottomMargin(0.15)
    gPad.SetRightMargin(0.2)

    gStyle.SetOptStat(0)

    #plots
    quark_strap.GetYaxis().SetRangeUser(-50,50)
    quark_strap.SetLineColor(2)
    quark_strap.SetLineStyle(2)
    quark_negative.SetLineColor(2)
    quark_negative.SetLineStyle(2)

    quark_use.SetLineColor(30)
    quark_use.SetLineStyle(2)
    quarkMC_negative.SetLineColor(30)
    quarkMC_negative.SetLineStyle(2)

    quark_show_use.SetLineColor(6)
    quark_show_use.SetLineStyle(2)
    quark_show_negative.SetLineColor(6)
    quark_show_negative.SetLineStyle(2)

    q_sigma_total.SetLineColor(4)
    q_sigma_total.SetLineStyle(1)
    q_sigma_total.SetLineWidth(2)
    neg_q_sigma_tot.SetLineColor(4)
    neg_q_sigma_tot.SetLineStyle(1)
    neg_q_sigma_tot.SetLineWidth(2)

    quark_strap.GetYaxis().SetTitle("Uncertainty (%)")
    quark_strap.GetYaxis().SetRangeUser(-50,50)
    quark_strap.Draw("HIST") #statistical uncertianty
    print("passes")
    quark_negative.Draw("HIST same") #stat uncertianty negative
    quark_use.Draw("HIST same") #mc closure
    quarkMC_negative.Draw("HIST same") #mc closure negative
    quark_show_use.Draw("HIST same") #showering
    quark_show_negative.Draw("HIST same") #showering negative
    q_sigma_total.Draw("HIST same") #total
    neg_q_sigma_tot.Draw("HIST same") #total negative

    leg = TLegend(0.82,0.7,0.98,0.9) ##0.6,0.5,0.9,0.7
    leg.SetTextFont(42)
    leg.SetFillColor(0)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)
    leg.SetNColumns(1)
    leg.AddEntry(quark_strap,"Statistical","l")
    leg.AddEntry(quark_use,"MC Closure","l")
    leg.AddEntry(quark_show_use,"Showering","l")
    leg.AddEntry(q_sigma_total,"Total","l")

    myText(0.18,0.9,"#it{#bf{#scale[1.5]{#bf{ATLAS} Simulation Preliminary}}}")
    myText(0.18,0.86,"#bf{#scale[1.5]{pT range: "+str(min)+" - "+str(max)+" GeV}}")
    myText(0.18,0.82,"#it{#bf{#scale[1.5]{Quark Jet}}}")
    leg.Draw()

    if(inputvar == "ntrk"):
        line = TLine(0.,0,60,0)
        quark_strap.GetXaxis().SetTitle("n_{Track}")

    if(inputvar == "bdt"):
        line = TLine(-0.8,0,0.7,0)
        quark_strap.GetXaxis().SetTitle("BDT")
    line.Draw("same")
    c.Print("./plots/gamma+/total_mc/plots_" + var + "/" + str(min) + "quark_total.pdf")

##### gluon
    gluon_strap.GetYaxis().SetRangeUser(-50,50)
    gluon_strap.SetLineColor(2)
    gluon_strap.SetLineStyle(2)
    gluon_negative.SetLineColor(2)
    gluon_negative.SetLineStyle(2)

    gluon_use.SetLineColor(30)
    gluon_use.SetLineStyle(2)
    gluonMC_negative.SetLineColor(30)
    gluonMC_negative.SetLineStyle(2)

    gluon_show_use.SetLineColor(6)
    gluon_show_use.SetLineStyle(2)
    gluon_show_negative.SetLineColor(6)
    gluon_show_negative.SetLineStyle(2)

    g_sigma_total.SetLineColor(4)
    g_sigma_total.SetLineStyle(1)
    g_sigma_total.SetLineWidth(2)
    neg_g_sigma_tot.SetLineColor(4)
    neg_g_sigma_tot.SetLineStyle(1)
    neg_g_sigma_tot.SetLineWidth(2)

    gluon_strap.GetYaxis().SetTitle("Uncertainty (%)")
    gluon_strap.GetYaxis().SetRangeUser(-50,50)
    gluon_strap.Draw("HIST") #statistical uncertianty

    gluon_negative.Draw("HIST same") #stat uncertianty negative
    gluon_use.Draw("HIST same") #mc closure
    gluonMC_negative.Draw("HIST same") #mc closure negative
    gluon_show_use.Draw("HIST same") #showering
    gluon_show_negative.Draw("HIST same") #showering negative
    g_sigma_total.Draw("HIST same") #total
    neg_g_sigma_tot.Draw("HIST same") #total negative

    leg = TLegend(0.82,0.7,0.98,0.9) ##0.6,0.5,0.9,0.7
    leg.SetTextFont(42)
    leg.SetFillColor(0)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)
    leg.SetNColumns(1)
    leg.AddEntry(gluon_strap,"Statistical","l")
    leg.AddEntry(gluon_use,"MC Closure","l")
    leg.AddEntry(gluon_show_use,"Showering","l")
    leg.AddEntry(g_sigma_total,"Total","l")

    myText(0.18,0.9,"#it{#bf{#scale[1.5]{#bf{ATLAS} Simulation Preliminary}}}")
    myText(0.18,0.86,"#bf{#scale[1.5]{pT range: "+str(min)+" - "+str(max)+" GeV}}")
    myText(0.18,0.82,"#it{#bf{#scale[1.5]{Gluon Jet}}}")
    leg.Draw()

    if(inputvar == "ntrk"):
        line = TLine(0.,0,60,0)
        gluon_strap.GetXaxis().SetTitle("n_{Track}")

    if(inputvar == "bdt"):
        line = TLine(-0.8,0,0.7,0)
        gluon_strap.GetXaxis().SetTitle("BDT")
    line.Draw("same")
    c.Print("./plots/gamma+/total_mc/plots_" + var + "/" + str(min) + "gluon_total.pdf")
