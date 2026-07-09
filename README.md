<p align="center">
  <img width="318" height="103" alt="Giris" src="https://github.com/user-attachments/assets/acd21841-ce88-4ec4-a48b-85cde63039e2" />
</p>
Herkese Selamlar

"Her" filmindeki "Samantha" yapay zekasından etkilenerek kendim için yaptığım arayüzü biraz revize ederek paylaşmak istedim. 
Oldukça sade ve kolay kullanılmasına gayret ettim. Şu adresten "https://aistudio.google.com" alacağınız bir APİ.Key anahtarını, uygulamanın ilk açılışında istenen yere girin ve kullanmaya başlayın. 
İsterseniz ayarlardan daha sonra başka key girerek değiştirebilirsiniz.
İster hemen mikrofona konuşarak, istersenizde kapsüle çift tıklayarak açılan metin alanına yazınızı yazarak sohbete başlayabilirisniz. Gemini sadece sesle yanıt verecektir.
Dediğim gibi oldukça sade yapmaya çalıştım. Ekran yakalama, Kamera vs. gibi özellikler çıkarılmıştır. Sadece sesli yanıt, sohbet içindir.
Maalesef Google canlı bağlantılarda (WebSocket) web araması için karmaşık OAuth 2.0 yetkilendirmesi dayattığından, "Google Arama" fonksiyonunu da çıkarmak zorunda kaldım. 
Bu sorunu çok uğraşmama rağmen çözemedim maalesef, o sebeple uygulamada kullandığım (Gemini 2.5 Flash Native Audio) model sadece 2023 yılına kadar günceldir, o tarihten sonrası yok... Eğer bu sorunu çözen veya çözümü bilen lütfen bana da söylerse sevinirim.
Ben kodlama bilen biri değilim, kodları tamamen yapay zekaya yaptırdım, o sebeple kusurlarımı mazur görün lütfen. "Gemini live" yeni gelişen bir teknoloji bildiğim kadarı ile ve bizde kodlarda "api_version": "v1alpha" kullanıyoruz.
Maalesef diğer modelleri çalıştıramadım. Bu sebeplerden ve token limitleri veya sunucu tarafındaki sorunlardan dolayı kesinti olabilir. Ben kendim test için 2 saate yakın kesintisiz konuşmuştum. Eğer kesilirse en azından uygulamayı tekrar başlatmayı deneyiniz, muhtemelen düzelecektir.
Dileyen dilediği gibi uygulamayı değiştirebilir, geliştirebilir veya ilham alıp kendi uygulamasına kullanabilir. Herkese sevgiler...

-------
English translation;

Hello Everyone,
Inspired by the "Samantha" AI from the movie "Her", I wanted to slightly revise and share the interface I originally built for myself. I tried to keep it as simple and user-friendly as possible. Just grab an API Key from "https://aistudio.google.com", enter it into the prompt when you first launch the app, and you're good to go. You can always change it later with a different key in the settings.
You can start chatting either by speaking into your microphone right away, or by double-clicking the capsule to open the chat box and typing your message. Gemini will respond with voice only. As I mentioned, I aimed for ultimate simplicity, so features like screen capture or camera access have been removed. It is strictly for voice-based conversations.
Unfortunately, because Google enforces complex OAuth 2.0 authorization for web searches over live connections (WebSocket), I had to remove the "Google Search" function as well. Despite my best efforts, I couldn't crack this issue. Therefore, the model I used (Gemini 2.5 Flash Native Audio) is only up to date until 2023; it lacks data after that... If anyone knows a workaround or a solution for this, please let me know, I'd appreciate it!
I am not a coder myself—I had AI write the entire codebase, so please excuse any flaws or shortcomings. As far as I know, "Gemini Live" is a newly developing technology, and we are using "api_version": "v1alpha" in the code. I couldn't get the other models to work. Due to these reasons, token limits, or server-side issues, you might experience occasional disconnections. During my personal tests, I managed to chat continuously for nearly 2 hours. If it disconnects, just try restarting the app; it will most likely fix itself.
Feel free to modify, improve, or take inspiration from this app for your own projects. Sending love to everyone...

-------

### 🚀 Kısaca bazı özellikler / Quick Features:

* 🖱️ **Sürükle ve Taşı (Drag and Move):** Kapsülü farenizle (mouse) basılı tutarak ekranın istediğiniz yerine rahatça taşıyabilirsiniz. / Click and hold the capsule with your mouse to drag and position it anywhere on your screen.

* 🎙️ **Aç/Kapa için Sadece Tıkla (Just Click to Toggle):** Mikrofonu tek bir tıklamayla aktif veya sessiz hale getirebilirsiniz. / Easily mute or unmute the microphone with a single click.

<img width="319" height="171" alt="Mik durumu" src="https://github.com/user-attachments/assets/330a2126-d772-45c9-99db-7033ce03abb6" />

* 💬 **Çift Tıkla-Aç Chat Kutusu (Double-Click Chat Box):** Kapsüle çift tıklayarak metin alanını açabilir, yazılı olarak da iletişim kurabilirsiniz. / Double-click the capsule to open the text input and type your messages.

<img width="317" height="189" alt="Metin Kutusu" src="https://github.com/user-attachments/assets/6aac26df-cb96-4340-a59d-624bd927a594" />

* ⚙️ **Gelişmiş Ayarlar Menüsü (Advanced Settings):** API anahtarı değişimi, yapay zekanın ses seçimi, dil seçimi ve yapay zekaya rol biçebileceğiniz sistem talimatı (System Instruction) alanını içerir. / Includes API key updates, AI voice selection, language selection, and a system instruction field to define the AI's persona.

<img width="318" height="429" alt="Ayarlar" src="https://github.com/user-attachments/assets/59778fdf-72a3-45f4-97a4-ffbce5bca658" />

* ⌨️ **ESC ile Hızlı Gizleme (Quick Hide with ESC):** Ekranda yer kaplamasını istemediğinizde ESC tuşuna basarak uygulamayı anında gizleyebilirsiniz. / Instantly hide the app by pressing the ESC key whenever you need it out of sight.




<p align="center">
  <a href="https://www.youtube.com/watch?v=vDMtb-2wz4A">
    <img src="https://img.youtube.com/vi/vDMtb-2wz4A/hqdefault.jpg" alt="Seminay AI - Gemini Live Masaüstü Uygulaması Demo" width="240" height="180" style="border-radius: 6px; border: 1px solid #ddd; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
  <br>
  <strong>🎬 Seminay AI: Gemini Live Desktop Demo</strong>
  </a>
</p>



<p align="center">
  <!-- GitHub Release Butonu -->
  <a href="https://github.com/Zgrxxx/Seminay-AI/releases/latest">
    <img src="[https://img.shields.io/badge/Download-EXE_v1.0.0-green?style=for-the-badge&logo=windows](https://drive.google.com/file/d/1Baq60kXJmbsrBYB0_nJPns9eyuaoSrw_/view?usp=sharing)" alt="Download EXE">
  </a>
</p>




<p align="center">
  🔗 <b>Alternatif İndirme Linki / Alternative Download Link (Google Drive):</b> 
  <a href="https://drive.google.com/file/d/1Sxemtt7pdiDz81_v4-8ay8jZFPVlqE9q/view?usp=sharing">İndir / Download</a>
</p>
  </a>
</p>
