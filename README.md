# Hüquq çatbotu

Əmək məcəlləsi ilə bağlı suallar verə biləcəyiniz hüquq çatbotudur.

Üstünlükləri:
* Vektorlaşdırma modeli açıq mənbəlidir və heç bir bulud həllindən asılı deyil.
* LangChain və LLaMAIndex kimi böyük kitabxanalardan istifadə olunmayıb. Bütün mərhələlər mümkün olduğu qədər təmiz Python ilə və ya Numpy və FAISS kimi daha fundamental kitabxanalar ilə yazılıb.

Boşluqlar:
* Dil modeli kimi GPT-3.5-Turbo istifadə olunur. Bu layihədə istifadə olunan tək bulud həllidir. İstifadəsi üçün OpenAI API açarı lazımdır.
* Eyni anda yalnız bir qanun üçün işləyir.
* Çat tarixçəsi yoxudur. Hər sual ayrıca nəzərə alınır (tarixçə əlavə etmək asandır, keyfiyyətli şəkildə etmək isə çətin).

## Quraşdırma

```sh
git clone https://github.com/ceferisbarov/eqanun-rag-sample

cd eqanun-rag-sample

python3 -m venv env

source env/bin/activate

pip install -r requirements.txt
```

Aşağıdakı formada `.env` faylı yaradın:
```sh
OPENAI_API_KEY="your_openai_token"
HF_TOKEN="your_hf_token"
TOKENIZERS_PARALLELISM="true"
DOCUMENT_ID="46943"
DOCUMENT_NAME="Əmək Məcəlləsi"
```
DOCUMENT_ID istədiyiniz məcəllənin e-qanun vebsaytındakı id-si ilə eyni olmalıdır. Ad da eyni şəkildə. OpenAI və Hugging Face tokenlərini öz hesabınızda yaradıb bura əlavə etməyiniz lazımdır. HF_TOKEN eqanun datasetini yükləmək üçün, OPENAI_API_KEY isə GPT modellərindən istifadə etmək üçün lazımdır.

## Növbəti işlər
- [ ] Layihəni konteynerlərşdirmək.
- [ ] Windows dəstəyi (baxın: birinci)
- [ ] 