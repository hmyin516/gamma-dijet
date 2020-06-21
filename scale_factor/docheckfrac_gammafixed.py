from ROOT import *
import numpy as np

doreweight = 0
inputvar = "ntrk"
mc = "sherpa_SF"
var = inputvar
ntrackall = TFile("ROOT/dijet_sherpa_py_forGamma.root")
ntrackall3  = TFile("ROOT/dijet_data_py_forGamma.root")
gammasherpa = TFile("ROOT/gammajet_sherpa.root")
gammadata = TFile("ROOT/gammajet_data.root")

def myText(x,y,text,color =1):
    l = TLatex()
    l.SetTextSize(0.025)
    l.SetNDC()
    l.SetTextColor(color)
    l.DrawLatex(x,y,text)
    pass

bin = [0,50,100,150,200,300,400,500,600,800,1000,1200,1500,2000]
for i in range(1,7):   #for only dijet event, start from jet pT>500 GeV
#for i in range(13):	#for gamma+jet combined with dijet event, start from jet pT>0 GeV
    min = bin[i]
    max = bin[i+1]

    dijet_quark = ntrackall.Get(str(min)+"_LeadingJet_Forward_Quark_"+inputvar)
    dijet_subjetquark = ntrackall.Get(str(min)+"_SubJet_Forward_Quark_"+inputvar)

    dijet_gluon = ntrackall.Get(str(min)+"_LeadingJet_Forward_Gluon_"+inputvar)
    dijet_subjetgluon = ntrackall.Get(str(min)+"_SubJet_Forward_Gluon_"+inputvar)

    dijet_quark2 = ntrackall.Get(str(min)+"_LeadingJet_Central_Quark_"+inputvar)
    dijet_subjetquark2 = ntrackall.Get(str(min)+"_SubJet_Central_Quark_"+inputvar)

    dijet_gluon2 = ntrackall.Get(str(min)+"_LeadingJet_Central_Gluon_"+inputvar)
    dijet_subjetgluon2 = ntrackall.Get(str(min)+"_SubJet_Central_Gluon_"+inputvar)

    gamma_quark = gammasherpa.Get(str(min) + "_LeadingJet_Central_Quark_" + inputvar)
    gamma_gluon = gammasherpa.Get(str(min) + "_LeadingJet_Central_Gluon_" + inputvar)



    dijet_data1 = ntrackall3.Get(str(min)+"_LeadingJet_Forward_Data_"+inputvar)
    dijet_data2 = ntrackall3.Get(str(min)+"_LeadingJet_Central_Data_"+inputvar)

    dijet_data3 = ntrackall3.Get(str(min)+"_SubJet_Forward_Data_" + inputvar)
    dijet_data4 = ntrackall3.Get(str(min)+"_SubJet_Central_Data_" + inputvar)

    gamma_data = gammadata.Get(str(min)+"_LeadingJet_Central_Data_"+inputvar)



    dijet_data1.Add(dijet_data2)
    dijet_data3.Add(dijet_data4)
    #Leading jets only,no matter forward ro central
    for a in range(60):
		if np.isnan(dijet_quark.GetBinContent(a)):
			dijet_quark.SetBinContent(a,0)
		if np.isnan(dijet_quark2.GetBinContent(a)):
			dijet_quark2.SetBinContent(a,0)

    dijet_quark.Add(dijet_quark2)
   # lower_quark = dijet_quark


    for b in range(60):
		if np.isnan(dijet_gluon.GetBinContent(b)):
			dijet_gluon.SetBinContent(b,0)
		if np.isnan(dijet_gluon2.GetBinContent(b)):
			dijet_gluon2.SetBinContent(b,0)

    dijet_gluon.Add(dijet_gluon2)
   # lower_gluon = dijet_gluon

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
    dijet_data1.Add(dijet_data3)
    #reassigning to variables
    higher_quark = gamma_quark
    higher_gluon = gamma_gluon
    lower_quark = dijet_quark
    lower_gluon = dijet_gluon
    higher_data = gamma_data
    lower_data = dijet_data1



    #add leading and subleading jet from only dijet event together,
    #note that for gammajet+dijet event, we need to add leading jet from gammajet and leading jet from dijet sample together
   # higher_data.Add(higher_data2)
   # lower_data.Add(lower_data2)
   # higher_quark.Add(higher_quark2)
   # higher_gluon.Add(higher_gluon2)

    ToT_Fq2 = 0.
    ToT_Fg2 = 0.

    ToT_Cq2 =0.
    ToT_Cg2 = 0.
    for j in range(1,lower_quark.GetNbinsX()+1):
		ToT_Fq2+=higher_quark.GetBinContent(j)  #dijetquark
		ToT_Cq2+=lower_quark.GetBinContent(j) #gammaquark
		ToT_Fg2+=higher_gluon.GetBinContent(j) #dijetlguon
		ToT_Cg2+=lower_gluon.GetBinContent(j)#gammagluon




    # calculate the fraction of forward(higher) / central(lower) quark or gluon jet
    print("checking fraction")
    if ((ToT_Fg2+ToT_Fq2) != 0):
		fg=ToT_Fg2/(ToT_Fg2+ToT_Fq2)
		cg=ToT_Cg2/(ToT_Cq2+ToT_Cg2)
    else:
		continue

    fq=1.-fg
    cq=1.-cg

    print(fg)
    print(cg)
    print(fq)
    print(cq)


    c = TCanvas("c","c",500,500)
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


    if (lower_quark.Integral() != 0):
        lower_quark.Scale(1./lower_quark.Integral())
    if(lower_gluon.Integral() != 0):
        lower_gluon.Scale(1./lower_gluon.Integral())
    if(higher_quark.Integral() != 0):
        higher_quark.Scale(1./higher_quark.Integral())
    if(higher_gluon.Integral() != 0):
        higher_gluon.Scale(1./higher_gluon.Integral())
    if(lower_data.Integral() != 0):
        lower_data.Scale(1./lower_data.Integral())
    if(higher_data.Integral() != 0):
        higher_data.Scale(1./higher_data.Integral())



    higher = higher_quark.Clone("")
    lower = higher_quark.Clone("")

    for i in range(1,higher.GetNbinsX()+1):
        higher.SetBinContent(i,fg*higher_gluon.GetBinContent(i)+fq*higher_quark.GetBinContent(i))
        lower.SetBinContent(i,cg*lower_gluon.GetBinContent(i)+cq*lower_quark.GetBinContent(i))
        pass

    #Now, let's solve.

    quark = higher_quark.Clone("")
    gluon = higher_quark.Clone("")
    quark_data = higher_data.Clone("")
    gluon_data = higher_data.Clone("")

    #Matrix method here
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
    for i in range(1,higher_data.GetNbinsX()+1):
        F = higher_data.GetBinContent(i)
        C = lower_data.GetBinContent(i)
        if((cg*fq-fg*cq) != 0):
            Q = -(C*fg-F*cg)/(cg*fq-fg*cq)
            G = (C*fq-F*cq)/(cg*fq - fg*cq)
            quark_data.SetBinContent(i,Q)
            gluon_data.SetBinContent(i,G)
        pass

    gPad.SetLeftMargin(0.15)
    gPad.SetTopMargin(0.05)
    gPad.SetBottomMargin(0.15)

    if "SF" in mc:
        quark_ratio = quark_data.Clone("")
        gluon_ratio = gluon_data.Clone("")
        quark_ratio.GetYaxis().SetTitle("Data/MC") #Data/MC
        gluon_ratio.GetYaxis().SetTitle("Data/MC") #Data/MC
    if "MC" in mc:
        quark_ratio = higher_quark.Clone("")
        gluon_ratio = higher_gluon.Clone("")
        quark_ratio.GetYaxis().SetTitle("MC Closure") #Data/MC
        gluon_ratio.GetYaxis().SetTitle("MC Closure") #Data/MC

    quark_ratio.Divide(quark)
    gluon_ratio.Divide(gluon)


    gStyle.SetOptStat(0)
    ######################## for ratio plot
    c.Divide(2,1)

    top = c.cd(1)
    top.SetPad(0.0,0.0,1.0,1.0)
    top.SetFillColor(0)
    top.SetBorderMode(0)
    top.SetBorderSize(2)
    top.SetTickx(1)
    top.SetTicky(1)
    top.SetLeftMargin(0.14)
    top.SetRightMargin(0.055)
    top.SetBottomMargin(0.3)#0.25
    top.SetFrameBorderMode(0)
    #top.SetLogy(1)

    bot = c.cd(2)
    bot.SetPad(0.0,0.0,1.0,0.3)
    bot.SetFillColor(0)
    bot.SetBorderMode(0)
    bot.SetBorderSize(2)
    bot.SetTickx(1)
    bot.SetTicky(1)
    bot.SetLeftMargin(0.14)
    bot.SetRightMargin(0.055)
    bot.SetTopMargin(0.045)
    bot.SetBottomMargin(0.4)
    bot.SetFrameBorderMode(0)

    quark.SetTitle("")
    quark.GetXaxis().SetTitle(var)
    quark.GetYaxis().SetTitle("Normalized to unity")
    quark.GetYaxis().SetNdivisions(505)
    quark.GetYaxis().SetRangeUser(-0.01,quark.GetMaximum()*1.5)
    #quark.GetYaxis().SetRangeUser(-0.01,0.05)
    quark.SetMarkerColor(8)
    quark.SetLineColor(8)
    quark.SetMarkerSize(0.5)
    quark.SetMarkerStyle(20)


    quark_data.SetMarkerColor(1)
    quark_data.SetLineColor(1)
    quark_data.SetMarkerSize(0.8)
    quark_data.SetMarkerStyle(29)

    higher_quark.SetMarkerColor(2)
    higher_quark.SetLineColor(2)
    higher_quark.SetMarkerSize(0.5)
    higher_quark.SetMarkerStyle(21)

    lower_quark.SetMarkerColor(4)
    lower_quark.SetLineColor(4)
    lower_quark.SetMarkerSize(0.5)
    lower_quark.SetMarkerStyle(22)


    quark_ratio.SetTitle("")
    quark_ratio.GetYaxis().SetRangeUser(0.7,1.3)
    quark_ratio.GetXaxis().SetTitle(var)
    quark_ratio.GetXaxis().SetTitleOffset(1)
    quark_ratio.GetXaxis().SetTitleSize(0.11)
    quark_ratio.GetXaxis().SetLabelSize(0.1)
    quark_ratio.GetXaxis().SetLabelOffset(0.03)
    quark_ratio.GetYaxis().SetTitleSize(0.1)
    quark_ratio.GetYaxis().SetTitleOffset(0.5)
    #quark_ratio.GetYaxis().SetLabelSize(0.2)
    quark_ratio.GetYaxis().SetLabelOffset(0.01)

    top.cd()
    quark.Draw()
    if "SF" in mc:
		quark_data.Draw("same")
    if "MC" in mc:
         higher_quark.Draw("same")
       # lower_quark.Draw("same")
		#higher_data.Draw("same")
		#lower_data.Draw("same")
    if "bdt" in inputvar:
        leg = TLegend(0.75,0.57,0.94,0.67)
        line = TLine(-0.8,1,0.7,1)
    if "ntrk" in inputvar:
        leg = TLegend(0.55,0.55,0.82,0.65)
        line = TLine(0,1,60,1)
    else:
        leg = TLegend(0.55,0.55,0.82,0.65)
        line = TLine(0,1,60,1)
    leg.SetTextFont(42)
    leg.SetFillColor(0)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)
    leg.SetNColumns(1)
    leg.AddEntry(quark,"Extracted quark (mc)","p")
    if "SF" in mc:
        myText(0.18,0.84,"#it{#bf{#scale[1.8]{#bf{ATLAS} Internal}}}")
        leg.AddEntry(quark_data,"Extracted quark (data)","p")
    if "MC" in mc:
        leg.AddEntry(higher_quark,"gamma quark (mc)","p")
        myText(0.18,0.84,"#it{#bf{#scale[1.8]{#bf{ATLAS} Simulation Internal}}}")
    leg.Draw()

    myText(0.18,0.80,"#bf{#scale[1.5]{#sqrt{s} = 13 TeV}}")
    myText(0.18,0.75,"#bf{#scale[1.5]{pT range: "+str(min)+" - "+str(max)+" GeV}}")


   # line = TLine(0.,1,60,1)
   # line = TLine(-0.8,1,0.7,1)
    #line = TLine(0.,1,0.4,1)

    bot.cd()
    quark_ratio.Draw()
    line.Draw("same")
    #c.Print("./plots_bdt/quark_"+str(min)+"_"+str(doreweight)+"_"+mc+"_"+var+"_fc.pdf")
    c.Print("./plots/gamma+/2d1g/plots_"+var+"/quark/quark_"+str(min)+"_"+str(doreweight)+"_"+mc+"_"+var+".pdf")
    #c.Print("./plots/gamma+/truthMC/plots_"+var+"/quark/truth_MC_quark_"+str(min)+".pdf")

    gluon.SetTitle("")
    gluon.GetXaxis().SetTitle(var)
    gluon.GetYaxis().SetTitle("Normalized to unity")
    gluon.GetYaxis().SetNdivisions(505)
    #gluon.GetYaxis().SetRangeUser(-0.01,0.05)
    gluon.GetYaxis().SetRangeUser(-0.01,gluon.GetMaximum()*1.75)
    gluon.SetMarkerColor(8)
    gluon.SetLineColor(8)
    gluon.SetMarkerSize(0.5)
    gluon.SetMarkerStyle(20)

    gluon_data.SetMarkerColor(1)
    gluon_data.SetLineColor(1)
    gluon_data.SetMarkerSize(0.8)
    gluon_data.SetMarkerStyle(29)

    higher_gluon.SetMarkerColor(2)
    higher_gluon.SetLineColor(2)
    higher_gluon.SetMarkerSize(0.5)
    higher_gluon.SetMarkerStyle(21)

    lower_gluon.SetMarkerColor(4)
    lower_gluon.SetLineColor(4)
    lower_gluon.SetMarkerSize(0.5)
    lower_gluon.SetMarkerStyle(22)


    gluon_ratio.SetTitle("")
    gluon_ratio.GetYaxis().SetRangeUser(0.7,1.3)
    gluon_ratio.GetXaxis().SetTitle(var)
    gluon_ratio.GetXaxis().SetTitleOffset(1)
    gluon_ratio.GetXaxis().SetTitleSize(0.11)
    gluon_ratio.GetXaxis().SetLabelSize(0.1)
    gluon_ratio.GetXaxis().SetLabelOffset(0.03)
    gluon_ratio.GetYaxis().SetTitleSize(0.1)
    gluon_ratio.GetYaxis().SetTitleOffset(0.5)
    #gluon_ratio.GetYaxis().SetLabelSize(0.2)
    gluon_ratio.GetYaxis().SetLabelOffset(0.01)


    top.cd()
    gluon.Draw()
    if "SF" in mc:
        gluon_data.Draw("same")
    if "MC" in mc:
        higher_gluon.Draw("same")
    #lower_gluon.Draw("same")
    #higher_data.Draw("same")
    #lower_data.Draw("same")
    if "bdt" in inputvar:
        leg = TLegend(0.15,0.55,0.42,0.65)
        line = TLine(-0.8,1,0.7,1)
    if "ntrk" in inputvar:
        leg = TLegend(0.55,0.55,0.82,0.65)
        line = TLine(0,1,60,1)##0.6,0.5,0.9,0.7
    #leg = TLegend(0.6,0.5,0.9,0.7) ##0.6,0.5,0.9,0.7
    leg.SetTextFont(42)
    leg.SetFillColor(0)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)
    leg.SetNColumns(1)
    leg.AddEntry(gluon,"Extracted gluon (mc)","p")
    if "SF" in mc:
        leg.AddEntry(gluon_data,"Extracted gluon (data)","p")
        myText(0.18,0.84,"#it{#bf{#scale[1.8]{#bf{ATLAS} Internal}}}")
    if "MC" in mc:
        myText(0.18,0.84,"#it{#bf{#scale[1.8]{#bf{ATLAS} Simulation Internal}}}")
        leg.AddEntry(higher_gluon,"gamma gluon (mc)","p")
    #leg.AddEntry(lower_gluon,"lower gluon (mc)","p")
    leg.Draw()

    myText(0.18,0.80,"#bf{#scale[1.5]{#sqrt{s} = 13 TeV}}")
    myText(0.18,0.75,"#bf{#scale[1.5]{pT range: "+str(min)+" - "+str(max)+" GeV}}")


   # line = TLine(0.,1,60,1)
   # line = TLine(-0.8,1,0.7,1)
    #line = TLine(0.,1,0.4,1)

    bot.cd()
    gluon_ratio.Draw()
    line.Draw("same")
    #c.Print("./plots/gamma+/truthMC/plots_"+var+"/gluon/truth_MC_gluon_"+str(min)+".pdf")
   c.Print("./plots/gamma+/2d1g/plots_"+var+"/gluon/gluon_"+str(min)+"_"+str(doreweight)+"_"+mc+"_"+var+".pdf")
