<p align="center">
  <img width="318" height="103" alt="Giris" src="https://github.com/user-attachments/assets/acd21841-ce88-4ec4-a48b-85cde63039e2" />
</p>
Herkese Selamlar

"Her" filmindeki "Samantha" yapay zekasından etkilenerek kendim için yaptığım arayüzü biraz revize ederek paylaşmak istedim. 
Oldukça sade ve kolay kullanılmasına gayret ettim. Şu adresten "https://aistudio.google.com" alacağınız ücretsiz bir APİ.Key anahtarını, uygulamanın ilk açılışında istenen yere girin ve kullanmaya başlayın. 
İsterseniz ayarlardan daha sonra başka key girerek değiştirebilirsiniz.

İster hemen mikrofona konuşarak, istersenizde kapsüle çift tıklayarak açılan metin alanına yazınızı yazarak sohbete başlayabilirisniz. Gemini sadece sesle yanıt verecektir.
Dediğim gibi oldukça sade yapmaya çalıştım. Ekran yakalama, Kamera vs. gibi özellikler çıkarılmıştır. Sadece sesli yanıt, sohbet içindir. (Lakin istenirse belki gelecekte eklenebilir.)

Ben kodlama bilen biri değilim, kodları tamamen yapay zekaya yaptırdım, o sebeple kusurlarımı mazur görün lütfen. "Gemini live" yeni gelişen bir teknoloji bildiğim kadarı ile ve bizde kodlarda model: "gemini-2.5-flash-native-audio-latest" ve "api_version": "v1alpha" kullanıyoruz.

Maalesef diğer modelleri çalıştıramadım. Bu sebeplerden ve token limitleri veya sunucu tarafındaki sorunlardan dolayı kesinti olabilir. Eğer kesilirse en azından uygulamayı tekrar başlatmayı deneyiniz, muhtemelen düzelecektir.

Dileyen dilediği gibi uygulamayı değiştirebilir, geliştirebilir veya ilham alıp kendi uygulamasına kullanabilir, sizlerin takdirine kalmış... Herkese sevgiler...

-------
English translation;

Greetings Everyone,

I wanted to share the interface I built for myself, inspired by the AI "Samantha" from the movie "Her," after making a few revisions to it. 

I tried to keep it as simple and user-friendly as possible. Just get a free API Key from "https://aistudio.google.com", enter it into the prompt when you first launch the app, and you're good to go.

If you wish, you can change it later by entering a different key in the settings.

You can start the conversation either by speaking into the microphone right away or by double-clicking the capsule to type your message in the text field that appears. Gemini will only respond via voice.

As I mentioned, I tried to keep it quite minimal. Features like screen capture, camera, etc., have been removed. It is strictly for voice-based responses and chatting. (However, they might be added in the future if requested.)

I am not someone who knows how to code; I had AI write the code entirely, so please overlook any flaws. As far as I know, "Gemini Live" is an emerging technology, and we are using "gemini-2.5-flash-native-audio-latest" and "api_version": "v1alpha" in the code.

Unfortunately, I couldn't get the other models to work. Due to these reasons, token limits, or server-side issues, there might be occasional interruptions. If it disconnects, try restarting the app at the very least; it will likely fix the issue.

Anyone is welcome to modify, improve, or take inspiration from this app for their own projects however they see fit—it's entirely up to you... Much love to everyone...

-------

### 🚀 Kısaca bazı özellikler / Quick Features:

* 🖱️ **Sürükle ve Taşı (Drag and Move):** Kapsülü farenizle (mouse) basılı tutarak ekranın istediğiniz yerine rahatça taşıyabilirsiniz. / Click and hold the capsule with your mouse to drag and position it anywhere on your screen.

* 🎙️ **Aç/Kapa için Sadece Tıkla (Just Click to Toggle):** Mikrofonu tek bir tıklamayla aktif veya sessiz hale getirebilirsiniz. / Easily mute or unmute the microphone with a single click.

<img width="319" height="171" alt="Mik durumu" src="https://github.com/user-attachments/assets/330a2126-d772-45c9-99db-7033ce03abb6" />

* 💬 **Çift Tıkla-Aç Chat Kutusu (Double-Click Chat Box):** Kapsüle çift tıklayarak metin alanını açabilir, yazılı olarak da iletişim kurabilirsiniz. / Double-click the capsule to open the text input and type your messages.

<img width="317" height="189" alt="Metin Kutusu" src="https://github.com/user-attachments/assets/6aac26df-cb96-4340-a59d-624bd927a594" />

* ⚙️ **Gelişmiş Ayarlar Menüsü (Advanced Settings):** API anahtarı değişimi, yapay zekanın ses tonu ve dil seçimi, mikrofon ile hoparlör tercihi, bas-konuş tuş ataması ve yapay zekaya rol biçebileceğiniz sistem talimatı (System Instruction) alanını içerir. / Includes API key updates, AI voice and language selection, microphone and speaker preferences, push-to-talk key assignment, and a system instruction field to define the AI's persona.

<img width="308" height="512" alt="Ayarlar" src="https://github.com/user-attachments/assets/442be9e6-8161-4e4b-a4d5-6416d9e1563d" />

* ⌨️ **ESC ile Gizleme & Ctrl+F9 ile Çağırma (Quick Hide & Summon):** Ekranda yer kaplamasını istemediğinizde ESC tuşuna basarak uygulamayı anında gizleyebilir, Ctrl+F9 kısayolu sayesinde ise dilediğiniz her yerden uygulamayı anında ekranın önüne geri çağırabilirsiniz. / Instantly hide the app by pressing the ESC key, and summon it back to the front from anywhere at any time using the Ctrl+F9 shortcut.

* 🎙️ **Bas-Konuş Modu (Push-to-Talk):** Ayarlar menüsünden dilediğiniz bir kısayol tuşu atadıktan sonra, kapsül üzerindeki mikrofonu tıklayarak sessize (kırmızı duruma) getirmenizle birlikte bas-konuş modu aktifleşir. Bu modda, yapay zeka ile sadece belirlediğiniz tuşa basılı tuttuğunuz sürece konuşabilirsiniz; tuşu bıraktığınızda mikrofon otomatik olarak tekrar sessize alınır. / Once you assign a hotkey in the settings menu, you can activate Push-to-Talk mode simply by muting the microphone (turning the indicator red) on the capsule. In this mode, you can speak to the AI only while holding down your designated hotkey, and once released, the microphone automatically mutes again.

<img width="578" height="512" alt="Yeni ayarlar" src="https://github.com/user-attachments/assets/21d75afd-0a65-4240-9d85-9ee176cfa4c5" />

-------
-------

Seminay AI v.1.0.1 - Güncelleme Notları

1. Bağlantı, hafıza ve Google arama sorununu çözdüğümü düşünüyorum. Bizzat 4,5 saat test ettim; uygulama açık olduğu sürece Google arama aktif, Gemini güncel bilgilere ulaşabilir, bağlantı tazelenir, kesinti hissedilmez ve hafıza yerindedir... (Not: Google yetki tokeni sınırlaması nedeniyle Gemini bazen arama gerektirecek soruda arayüzü "düşünüyor" modunda kilitleyecektir. Bu şekilde olunca tekrar seslenin ona; bu, bağlantıyı ve arama limitini tazeler ve kaldığınız yerden sohbete devam edebilirsiniz.)

2. Veri gönderim metodu, Google'ın istediği güncel metoda çekildi.

3. Bazı kod ve arayüz iyileştirme ve geliştirmeleri yapıldı. (Şeffaf arka plan, sürükleme ve gölge efekti vb...)

---

Seminay AI v.1.0.1 - Update Notes

1. I believe I have resolved the connection, memory, and Google Search issues. I personally tested it for 4.5 hours; as long as the application remains open, Google Search is active, Gemini can access up-to-date information, the connection refreshes, there is no noticeable interruption, and the memory remains intact... (Note: Due to Google authorization token limitations, Gemini may occasionally lock the interface in "thinking" mode when a query requires a search. If this happens, simply speak to it again; this will refresh the connection and search limits, allowing you to continue the conversation from where you left off.)

2. The data transmission method has been updated to the current method required by Google.

3. Various code and interface improvements were made. (Transparent background, dragging, shadow effects, etc.)

-------
-------

Seminay AI v1.0.2 - Güncelleme Notları

1. Bas-Konuş Özelliği Eklendi: Artık mikrofonu kapsül üzerinden kapattığınız (sessize aldığınız) an bas-konuş özelliği devreye girer. Ayarlar menüsünden dilediğiniz bir kısayol tuşunu atayarak kullanmaya başlayabilirsiniz.

2. Gelişmiş Kısayollar (Ctrl+F9): ESC tuşu ile gizlediğiniz uygulamayı, artık dilediğiniz her yerden Ctrl+F9 kısayolunu kullanarak anında ekranın önüne geri çağırabilirsiniz.

3. Ses Cihazı Seçimi: Farklı senaryolar ve donanımlar için mikrofon ve hoparlör seçim alanları ayarlar menüsüne eklendi.

4. Bağlantı Durum Bildirimi: İnternet veya sunucu bağlantısı koptuğunda, kapsül hareketsiz kalıp kırmızı renge bürünerek anlık görsel geri bildirim sağlar.

<img width="137" height="62" alt="Kapalı 1" src="https://github.com/user-attachments/assets/7db2a55c-4c8c-44e2-9e26-615059dfb48f" />

5. Kod İyileştirmeleri: Dinamik dosya/ikon yönetimi, ayarlar panelinin görsel düzenlemeleri ve arka plandaki ufak tefek hataların giderilmesine yönelik kararlılık güncellemeleri yapıldı.

Seminay AI v1.0.2 - Release Notes

1. Push-to-Talk Feature Added: Once you mute the microphone on the capsule, the push-to-talk feature is activated. You can assign your own hotkey in the settings menu to start using it.

2. Advanced Shortcuts (Ctrl+F9): You can now instantly summon the app and bring it to the front from anywhere using the Ctrl+F9 shortcut after hiding it with ESC.

3. Audio Device Selection: Microphone and speaker selection options have been added to the settings menu for various scenarios and hardware.

4. Connection Status Notification: If the internet or server connection is lost, the capsule remains static and turns red to provide instant visual feedback.

<img width="137" height="62" alt="Kapalı" src="https://github.com/user-attachments/assets/ae10cb00-5900-4d4e-8930-87fa8c231ba7" />

5. Code Improvements: Stability updates have been made, including dynamic file/icon management, visual adjustments to the settings panel, and minor bug fixes.
-------


<p align="center">
  <a href="https://www.youtube.com/watch?v=didl5c3rd1A" target="_blank">
    <img src="https://img.youtube.com/vi/didl5c3rd1A/hqdefault.jpg" alt="Seminay AI - Gemini Live Masaüstü Uygulaması Demo" width="240" height="180" style="border-radius: 6px; border: 1px solid #ddd; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
  <br>
  <strong>🎬 Seminay AI: Gemini Live Desktop</strong>
  </a>
</p>



<p align="center">
  <a href="https://github.com/Zgrxxx/Seminay-AI/releases/tag/V1.0.2">
    <img src="https://img.shields.io/badge/Download-EXE_v1.0.2-green?style=for-the-badge&logo=windows" alt="Download EXE">
  </a>
</p>

<p align="center">
  🔗 <b>Alternatif İndirme Linki / Alternative Download Link (Google Drive):</b> 
  <a href="https://drive.google.com/file/d/15fUIK68nhgXn11wQX0LzQL28QRu7jt2H/view?usp=sharing">İndir / Download</a>
</p>
