%% init TX Hardware 
% load default HaLo config
[ halo ] = halo_defaultConfig('halo');

%% init TX Hardware    
halo_init_tx(halo); 

%% Generate arbitrary waveform
T=10000;%total number of samples
N=T/4;%signal burst length
Nu=N/4;%number of used subcarriers in OFDM signal

tx_signal=[ifft([sign(randn(Nu,1))+1i*sign(randn(Nu,1));zeros(N-Nu,1)]);zeros(T-N,1)];
figure(1);
subplot(2,1,1);
plot([real(tx_signal) imag(tx_signal)])
subplot(2,1,2);
plot(10*log10(abs(fft(tx_signal))));ylim([-40 10])

%% Transmit waveform
halo_sendSignal(halo, tx_signal);
halo_start_tx(halo);