Double_t fitFunction(Double_t *x,Double_t *par){
	return par[0]*(TMath::Freq((sqrt(x[0])-sqrt(par[1]))/(2*par[2])));
}
