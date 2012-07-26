{

#include "4z_histos_parameters.h"
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>

//Declaring variables..........................
FILE *in;
FILE *fit_par;
FILE *histo_par;
FILE *histo1;
FILE *histo2;
FILE *histo3;
FILE *histo4;

int error, n, i, k, integ[4], num[4], integral, dof;
double z_photo, z_real, mean, emean, sigma, esigma, counts, ecounts, chi;
float *vector1, *vector2, *vector3, *vector4;
char charbins[30];
//.............................................

in=fopen(fname_in, "r"); 
fit_par=fopen(fname_fit_par, "w");
//histo_par=fopen(fname_histo_par, "w");

//gROOT.ProcessLine(".L $HOME/routines/bootstrap.C");
gROOT.ProcessLine(".L $HOME/routines/rmserror.C");

TH2F *h2=new TH2F("h2", "zp-histos", n_bining, zp_min, zp_min+zp_range, n_bins_bining , zs_min , zs_min+zs_range);
TH1F *zp=new TH1F("zp","0.2<zp<0.9", 35, 0.2, 0.9);
TH1F *zs=new TH1F("zp","0.2<zs<0.9", 35, 0.2, 0.9);

error=fscanf(in, "%lf %lf\n", &z_photo, &z_real);
while(error != -1)
{
	h2.Fill(z_photo,z_real);	
	zp.Fill(z_photo);
	zs.Fill(z_real);
	error=fscanf(in, "%lf %lf\n", &z_photo, &z_real);
}
fclose(in);

//Construct the four vectors with the histograms.............................................
in=fopen(fname_in, "r"); //Open file where the histogram is written

vector1=(float*) calloc(h2.Integral(1,1,1,n_bins_bining),sizeof(float));
printf("int1=%d\n",h2.Integral(1,1,1,n_bins_bining));
vector2=(float*) calloc(h2.Integral(2,2,1,n_bins_bining),sizeof(float));
printf("int2=%d\n",h2.Integral(2,2,1,n_bins_bining));
vector3=(float*) calloc(h2.Integral(3,3,1,n_bins_bining),sizeof(float));
printf("int3=%d\n",h2.Integral(3,3,1,n_bins_bining));
vector4=(float*) calloc(h2.Integral(4,4,1,n_bins_bining),sizeof(float));
printf("int4=%d\n",h2.Integral(4,4,1,n_bins_bining));

TH1F *bin=new TH1F("bin","", n_bining, zp_min, zp_min+zp_range);
for(i=0; i<4; i++) num[i]=0;
error=fscanf(in, "%lf %lf\n", &z_photo, &z_real);

while(error != -1)
{	
	bin.Fill(z_photo);
	
	i=0;
	if(bin.GetBinContent(i+1)==1)
	{
		k=num[i];
		vector1[k]=z_real;
		num[i]++;
	}
	
	i=1;
	if(bin.GetBinContent(i+1)==1)
	{
		k=num[i];
		vector2[k]=z_real;
		num[i]++;
	}
	
	i=2;
	if(bin.GetBinContent(i+1)==1)
	{
		k=num[i];
		vector3[k]=z_real;
		num[i]++;
	}
	
	
	i=3;
	if(bin.GetBinContent(i+1)==1)
	{
		k=num[i];
		vector4[k]=z_real;
		num[i]++;
	}
	
	bin.Scale(0);
	
	error=fscanf(in, "%lf %lf\n", &z_photo, &z_real);
}
for(i=0; i<4; i++) printf("num[%d]=%d\n",i,num[i]);
fclose(in);

//Geting histogram..................................................
TH1F *gr1=new TH1F("gr1","0.45<zp<0.50", n_bins_bining, zs_min, zs_min+zs_range);
n=1;

//histo1=fopen("Nz1.txt","w");
for(i=0; i <= n_bins_bining+1; i++) //Loop to fill histogram
{
	gr1.Fill(h2.GetYaxis().GetBinCenter(i), h2.GetBinContent(n,i));
	//fprintf(histo1,"%f %f\n", h2.GetYaxis().GetBinCenter(i), h2.GetBinContent(n,i));
}
//fclose(histo1);
integ[0]=gr1.Integral(0,n_bins_bining+1);
printf("integ[0]=%d\n",integ[0]);
gr1.Fit("gaus");
gr1.GetFunction("gaus").SetLineColor(2);

//Get fit parameters.................................................
TF1 *fit= gr1.GetFunction("gaus");
Double_t counts=fit.GetParameter(0);
Double_t ecounts=fit.GetParError(0);
Double_t mean=fit.GetParameter(1);
Double_t emean=fit.GetParError(1);
Double_t sigma=fit.GetParameter(2);
Double_t esigma=fit.GetParError(2);
Double_t chi=fit.GetChisquare();
fprintf(fit_par,"%lf %lf %lf %lf %lf %lf %lf %d\n",counts, ecounts, mean,emean,sigma,esigma, chi, fit.GetNDF());
//k=num[0];
//fprintf(histo_par,"%d %f %lf %lf %lf %lf %lf %lf %lf %lf\n", k, (float)sqrt(k), mean(vector1,k), rms(vector1,k)/sqrt(k), rms(vector1,k), rmserror(vector1,k), gr1.GetSkewness(), bootstrapskewness(vector1,k,"./OUTPUT/PLOT/RESULTS/histo1"), gr1.GetKurtosis(), bootstrapkurtosis(vector1,k, "./OUTPUT/PLOT/RESULTS/histo1"));
//fprintf(histo_par,"%d %f %lf %lf %lf %lf %lf %lf %lf %lf\n", k, (float)sqrt(k), gr1.GetMean(), bootstrapmean(vector1,k,"./OUTPUT/PLOT/RESULTS/histo1"), gr1.GetRMS(), bootstraprms(vector1,k,"./OUTPUT/PLOT/RESULTS/histo1"), gr1.GetSkewness(), bootstrapskewness(vector1,k,"./OUTPUT/PLOT/RESULTS/histo1"), gr1.GetKurtosis(), bootstrapkurtosis(vector1,k, "./OUTPUT/PLOT/RESULTS/histo1"));

//Geting histogram..................................................
TH1F *gr2=new TH1F("gr2","0.50<zp<0.55", n_bins_bining, zs_min, zs_min+zs_range);
n=2;

//histo2=fopen("Nz2.txt","w");	
for(i=0; i <= n_bins_bining+1; i++) //Loop to fill histogram
{
	gr2.Fill(h2.GetYaxis().GetBinCenter(i), h2.GetBinContent(n,i));
	//fprintf(histo2,"%f %f\n", h2.GetYaxis().GetBinCenter(i), h2.GetBinContent(n,i));
}
//fclose(histo2);
integ[1]=gr2.Integral(0,n_bins_bining+1);
printf("integ[1]=%d\n",integ[1]);
gr2.Fit("gaus");
gr2.GetFunction("gaus").SetLineColor(3);

//Get fit parameters.................................................
TF1 *fit= gr2.GetFunction("gaus");
Double_t counts=fit.GetParameter(0);
Double_t ecounts=fit.GetParError(0);
Double_t mean=fit.GetParameter(1);
Double_t emean=fit.GetParError(1);
Double_t sigma=fit.GetParameter(2);
Double_t esigma=fit.GetParError(2);
Double_t chi=fit.GetChisquare();
fprintf(fit_par,"%lf %lf %lf %lf %lf %lf %lf %d\n",counts, ecounts, mean,emean,sigma,esigma, chi, fit.GetNDF());
//k=num[1];
//fprintf(histo_par,"%d %f %lf %lf %lf %lf %lf %lf %lf %lf\n", k, (float)sqrt(k),  mean(vector2,k), rms(vector2,k)/sqrt(k), rms(vector2,k), rmserror(vector2,k), gr2.GetSkewness(), bootstrapskewness(vector2,k,"./OUTPUT/PLOT/RESULTS/histo2"), gr2.GetKurtosis(), bootstrapkurtosis(vector2,k,"./OUTPUT/PLOT/RESULTS/histo2"));
//fprintf(histo_par,"%d %f %lf %lf %lf %lf %lf %lf %lf %lf\n", k, (float)sqrt(k),  gr2.GetMean(), bootstrapmean(vector2,k, "./OUTPUT/PLOT/RESULTS/histo2"), gr2.GetRMS(), bootstraprms(vector2,k,"./OUTPUT/PLOT/RESULTS/histo2"), gr2.GetSkewness(), bootstrapskewness(vector2,k,"./OUTPUT/PLOT/RESULTS/histo2"), gr2.GetKurtosis(), bootstrapkurtosis(vector2,k,"./OUTPUT/PLOT/RESULTS/histo2"));


//Geting histogram..................................................
TH1F *gr3=new TH1F("gr3","0.55<zp<0.60", n_bins_bining, zs_min, zs_min+zs_range);
n=3;

//histo3=fopen("Nz3.txt","w");	
for(i=0; i <= n_bins_bining+1; i++) //Loop to fill histogram
{
	gr3.Fill(h2.GetYaxis().GetBinCenter(i), h2.GetBinContent(n,i));
	//fprintf(histo3,"%f %f\n", h2.GetYaxis().GetBinCenter(i), h2.GetBinContent(n,i));
}
//fclose(histo3);
integ[2]=gr3.Integral(0,n_bins_bining+1);
printf("integ[2]=%d\n",integ[2]);
gr3.Fit("gaus");
gr3.GetFunction("gaus").SetLineColor(4);

//Get fit parameters.................................................
TF1 *fit= gr3.GetFunction("gaus");
Double_t counts=fit.GetParameter(0);
Double_t ecounts=fit.GetParError(0);
Double_t mean=fit.GetParameter(1);
Double_t emean=fit.GetParError(1);
Double_t sigma=fit.GetParameter(2);
Double_t esigma=fit.GetParError(2);
Double_t chi=fit.GetChisquare();
fprintf(fit_par,"%lf %lf %lf %lf %lf %lf %lf %d\n",counts, ecounts, mean,emean,sigma,esigma, chi, fit.GetNDF());
//k=num[2];
//fprintf(histo_par,"%d %f %lf %lf %lf %lf %lf %lf %lf %lf\n", k, (float)sqrt(k),  mean(vector3,k), rms(vector3,k)/sqrt(k), rms(vector3,k), rmserror(vector3,k), gr3.GetSkewness(), bootstrapskewness(vector3,k,"./OUTPUT/PLOT/RESULTS/histo3"), gr3.GetKurtosis(), bootstrapkurtosis(vector3,k,"./OUTPUT/PLOT/RESULTS/histo3"));
//fprintf(histo_par,"%d %f %lf %lf %lf %lf %lf %lf %lf %lf\n", k, (float)sqrt(k),  gr3.GetMean(), bootstrapmean(vector3,k,"./OUTPUT/PLOT/RESULTS/histo3"), gr3.GetRMS(), bootstraprms(vector3,k,"./OUTPUT/PLOT/RESULTS/histo3"), gr3.GetSkewness(), bootstrapskewness(vector3,k,"./OUTPUT/PLOT/RESULTS/histo3"), gr3.GetKurtosis(), bootstrapkurtosis(vector3,k,"./OUTPUT/PLOT/RESULTS/histo3"));

//Geting histogram..................................................
TH1F *gr4=new TH1F("gr4","0.60<zp<0.65", n_bins_bining, zs_min, zs_min+zs_range);
n=4;

//histo4=fopen("Nz4.txt","w");	
for(i=0; i <= n_bins_bining+1; i++) //Loop to fill histogram
{
	gr4.Fill(h2.GetYaxis().GetBinCenter(i), h2.GetBinContent(n,i));
	//fprintf(histo4,"%f %f\n", h2.GetYaxis().GetBinCenter(i), h2.GetBinContent(n,i));
}
//fclose(histo4);
integ[3]=gr4.Integral(0,n_bins_bining+1);
printf("integ[3]=%d\n",integ[3]);
gr4.Fit("gaus");
gr4.GetFunction("gaus").SetLineColor(6);

//Get fit parameters.................................................
TF1 *fit= gr4.GetFunction("gaus");
Double_t counts=fit.GetParameter(0);
Double_t ecounts=fit.GetParError(0);
Double_t mean=fit.GetParameter(1);
Double_t emean=fit.GetParError(1);
Double_t sigma=fit.GetParameter(2);
Double_t esigma=fit.GetParError(2);
Double_t chi=fit.GetChisquare();
fprintf(fit_par,"%lf %lf %lf %lf %lf %lf %lf %d\n",counts, ecounts, mean,emean,sigma,esigma, chi, fit.GetNDF());
//k=num[3];
//fprintf(histo_par,"%d %f %lf %lf %lf %lf %lf %lf %lf %lf\n", k, (float)sqrt(k),  mean(vector4,k), rms(vector4,k)/sqrt(k), rms(vector4,k), rmserror(vector4,k), gr4.GetSkewness(), bootstrapskewness(vector4,k,"./OUTPUT/PLOT/RESULTS/histo4"), gr4.GetKurtosis(), bootstrapkurtosis(vector4,k,"./OUTPUT/PLOT/RESULTS/histo4"));
//fprintf(histo_par,"%d %f %lf %lf %lf %lf %lf %lf %lf %lf\n", k, (float)sqrt(k),  gr4.GetMean(), bootstrapmean(vector4,k,"./OUTPUT/PLOT/RESULTS/histo4"), gr4.GetRMS(), bootstraprms(vector4,k,"./OUTPUT/PLOT/RESULTS/histo4"), gr4.GetSkewness(), bootstrapskewness(vector4,k,"./OUTPUT/PLOT/RESULTS/histo4"), gr4.GetKurtosis(), bootstrapkurtosis(vector4,k,"./OUTPUT/PLOT/RESULTS/histo4"));

fclose(fit_par);
//fclose(histo_par);

//Text box...................................
//pt = new TPaveText(0.7,0.55,0.8,0.65, "NDC");
		
//pt.SetTextSize(0.04); 
//pt.SetTextAlign(12);
		
//sprintf(charbins,"N_{z-spec bins}=%d",  n_bins_bining);

//pt.AddText(charbins);
		
		
//Setting a legend................................................
leg = new TLegend(0.7,0.65,0.875,0.85);  //coordinates are fractions
    
leg.SetTextSize(0.03);									 
																			  
leg.AddEntry(gr1,"0.45<z_{bpz}<0.50","l");
leg.AddEntry(gr2,"0.50<z_{bpz}<0.55","l");
leg.AddEntry(gr3,"0.55<z_{bpz}<0.60","l");
leg.AddEntry(gr4,"0.60<z_{bpz}<0.65","l");  // "l" means line

//Plotting..................................................................................
gr1.SetLineColor(2);
gr1.GetXaxis().CenterTitle(); //Centering the axis labels
gr1.GetYaxis().CenterTitle();
gr1.SetXTitle("z_{spec}"); //Seting the title of the axis Deltaz=z_bpz-z_real
gr1.SetYTitle("counts");
gr1.Draw();
gr2.SetLineColor(3);
gr2.Draw("same");
gr3.SetLineColor(4);
gr3.Draw("same");
gr4.SetLineColor(6);
gStyle.SetOptStat(0);
gStyle.SetOptTitle(kFALSE);
gr4.Draw("same");
leg.Draw("same");
//pt.Draw("same");

c1.SetLogy();
c1.Print(plot_path);

}

  

