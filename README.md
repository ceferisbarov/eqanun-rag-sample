# Hüquq çatbotu

Əmək məcəlləsi ilə bağlı suallar verə biləcəyiniz hüquq çatbotudur.

Üstünlükləri:
* Vektorlaşdırma modeli açıq mənbəlidir və heç bir bulud həllindən asılı deyil.
* LangChain və LLaMAIndex kimi böyük kitabxanalardan istifadə olunmayıb. Bütün mərhələlər mümkün olduğu qədər təmiz Python ilə və ya Numpy və FAISS kimi daha fundamental kitabxanalar ilə yazılıb.

Boşluqlar:
* Dil modeli kimi GPT-4-Turbo istifadə olunur. Bu layihədə istifadə olunan tək bulud həllidir. İstifadəsi üçün OpenAI API açarı lazımdır.
* Eyni anda yalnız bir qanun üçün işləyir.
* Çat tarixçəsi yoxudur. Hər sual ayrıca nəzərə alınır (tarixçə əlavə etmək asandır, keyfiyyətli şəkildə etmək isə çətin).
