import openai
import os
from dotenv import load_dotenv
import re
import psycopg2
from psycopg2 import sql
import os

# Cargar la API key desde el archivo .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")

# def analizar_noticia(texto_noticia):
#     prompt = f"""
#     Analyze the following news article and provide the requested information in a structured format. Use values between 0 and 1 for numerical ratings to facilitate database storage.

#     1. **Sentiment Analysis**:
#     - Provide the overall sentiment of the article as three values between 0 and 1: positive, negative, and neutral.
#     - Example format: "Positive: 0.4, Negative: 0.3, Neutral: 0.3"

#     2. **Political Bias**:
#     - Classify the political bias of the article as three values between 0 and 1: left, right, and neutral, with a brief justification for the classification.
#     - Example format: "Left: 0.6, Right: 0.2, Neutral: 0.2. Explanation: The article promotes progressive policies."

#     3. **Tone**:
#     - Describe the tone of the article (e.g., sensationalist, moderate, objective) and provide a value between 0 and 1 indicating the intensity of this tone.
#     - Example format: "Tone: moderate, Intensity: 0.5"

#     4. **Thematic Classification**:
#     - Identify the main category of the article: politics, economy, science, technology, sports, entertainment, or health.
#     - Additionally, provide any relevant subthemes if applicable.
#     - Example format: "Main Category: economy, Subtheme: stock markets"

#     5. **Tags**:
#     - Generate 3 to 5 tags that represent the main topics or keywords of the article. Tags should be consistent and suitable for categorization.
#     - Example format: "Tags: stock market, trade policy, US economy"

#     6. **Locations**:
#     - List any locations mentioned in the article, grouped by country or region if applicable.
#     - Example format: "Locations: USA - New York, China - Beijing"

#     7. **Summary**:
#     - Provide a brief summary of the article (2-3 sentences), capturing the main points.

#     8. **Fact Consistency**:
#     - Indicate whether the main claims of the article seem consistent with commonly known facts. Highlight any specific statements that may require further verification if necessary.
#     - Example format: "Fact Consistency: The main claims appear consistent with commonly known facts. The statement regarding the projected growth rate in China might require further verification."

#     9. **Translation**:
#     - Provide a translation of the title and summary in the following languages: Spanish, French, German, Portuguese, Chinese, and Arabic.
#     - Use the following format:
#         - Spanish: "Title: [translated title], Summary: [translated summary]"
#         - French: "Title: [translated title], Summary: [translated summary]"
#         - German: "Title: [translated title], Summary: [translated summary]"
#         - Portuguese: "Title: [translated title], Summary: [translated summary]"
#         - Chinese: "Title: [translated title], Summary: [translated summary]"
#         - Arabic: "Title: [translated title], Summary: [translated summary]"

#     **News Article Text**:
#     {texto_noticia}
#     """
    
#     try:
#         response = openai.chat.completions.create(
#             model="gpt-4o-mini",  # Usa el modelo que prefieras
#             messages=[{
#                 'role': "user",
#                 'content': prompt,
#             }],
#             max_tokens=2000,
#             temperature=0.5
#         )
#         return response.choices[0].message.content
#     except Exception as e:
#         print(f"Error al procesar la noticia: {e}")
#         return None


def analizar_noticia(texto_noticia):
    return """
    1. **Sentiment Analysis**: 
   - Positive: 0.3, Negative: 0.5, Neutral: 0.2

    2. **Political Bias**: 
    - Left: 0.2, Right: 0.6, Neutral: 0.2. Explanation: The article focuses on Trump's victory and his policies, highlighting both support and criticism, but leans towards a negative portrayal of his impact on democracy.

    3. **Tone**: 
    - Tone: objective, Intensity: 0.6

    4. **Thematic Classification**: 
    - Main Category: politics, Subtheme: presidential election, immigration, economic policy

    5. **Tags**: 
    - Tags: Trump, Harris, 2024 election, immigration policy, economic policy

    6. **Locations**: 
    - Locations: USA - Washington, Florida, Georgia, North Carolina, Michigan, Wisconsin, Pennsylvania, Ohio, Montana, West Virginia, Arizona, Nevada

    7. **Summary**: 
    - Donald J. Trump won the 2024 presidential election, defeating Vice President Kamala Harris amid a deeply divided nation. His victory is seen as a return to isolationism and a shift in economic policy, with significant implications for American democracy and governance.

    8. **Fact Consistency**: 
    - Fact Consistency: The main claims appear consistent with commonly known facts. The assertion regarding Trump's criminal conviction and the political landscape post-election aligns with recent historical events, although the implications for democracy may require deeper analysis.

    9. **Translation**:
    - Spanish: "Title: Trump gana las elecciones presidenciales de 2024, derrotando a Harris, Summary: Donald J. Trump ganó las elecciones presidenciales de 2024, derrotando a la vicepresidenta Kamala Harris en medio de una nación profundamente dividida. Su victoria se considera un regreso al aislamiento y un cambio en la política económica, con importantes implicaciones para la democracia y el gobierno estadounidense."
    - French: "Title: Trump remporte l'élection présidentielle de 2024, battant Harris, Summary: Donald J. Trump a remporté l'élection présidentielle de 2024, battant la vice-présidente Kamala Harris dans une nation profondément divisée. Sa victoire est perçue comme un retour à l'isolationnisme et un changement de politique économique, avec d'importantes implications pour la démocratie et la gouvernance américaines."
    - German: "Title: Trump gewinnt die Präsidentschaftswahl 2024 und besiegt Harris, Summary: Donald J. Trump gewann die Präsidentschaftswahl 2024 und besiegte Vizepräsidentin Kamala Harris in einer tief gespaltenen Nation. Sein Sieg wird als Rückkehr zum Isolationismus und als Wandel in der Wirtschaftspolitik angesehen, mit erheblichen Auswirkungen auf die amerikanische Demokratie und Regierungsführung."
    - Portuguese: "Title: Trump vence a eleição presidencial de 2024, derrotando Harris, Summary: Donald J. Trump venceu a eleição presidencial de 2024, derrotando a vice-presidente Kamala Harris em uma nação profundamente dividida. Sua vitória é vista como um retorno ao isolamento e uma mudança na política econômica, com importantes implicações para a democracia e a governança americana."
    - Chinese: "Title: 特朗普赢得2024年总统选举，击败哈里斯, Summary: 唐纳德·特朗普赢得了2024年总统选举，击败副总统卡马拉·哈里斯，国家深陷分裂。 他的胜利被视为回归孤立主义和经济政策的转变，对美国民主和治理产生重大影响。"
    - Arabic: "Title: ترامب يفوز بالانتخابات الرئاسية 2024، متغلبًا على هاريس، Summary: فاز دونالد ج. ترامب بالانتخابات الرئاسية 2024، متغلبًا على نائبة الرئيس كامالا هاريس في أمة منقسمة بشدة. يُنظر إلى انتصاره على أنه عودة إلى العزلة وتحول في السياسة الاقتصادية، مع تداعيات كبيرة على الديمقراطية الأمريكية والحكم."
    """

# Ejemplo de texto de noticia para probar la función
texto_ejemplo = """
Trump Wins 2024 Presidential Election, Defeating Harris

He played on fears of immigrants and economic worries to defeat Vice President Kamala Harris. His victory signaled the advent of isolationism, sweeping tariffs and score settling.

Donald J. Trump rode a promise to smash the American status quo to win the presidency for a second time, surviving a criminal conviction, indictments, an assassin’s bullet, accusations of authoritarianism and an unprecedented switch of his opponent to complete a remarkable return to power.
Mr. Trump’s victory caps the astonishing political comeback of a man who was charged with plotting to overturn the last election but who tapped into frustrations and fears about the economy and illegal immigration to defeat Vice President Kamala Harris.
His defiant plans to upend the country’s political system held appeal to tens of millions of voters who feared that the American dream was drifting further from reach and who turned to Mr. Trump as a battering ram against the ruling establishment and the expert class of elites.
In a deeply divided nation, voters embraced Mr. Trump’s pledge to seal the southern border by almost any means, to revive the economy with 19th-century-style tariffs that would restore American manufacturing and to lead a retreat from international entanglements and global conflict.
Now, Mr. Trump will serve as the 47th president four years after reluctantly leaving office as the 45th, the first politician since Grover Cleveland in the late 1800s to lose re-election to the White House and later mount a successful run. At the age of 78, Mr. Trump has become the oldest man ever elected president, breaking a record held by President Biden, whose mental competence Mr. Trump has savaged.
His win ushers in an era of uncertainty for the nation.
To roughly half the country, Mr. Trump’s rise portends a dark turn for American democracy, whose future will now depend on a man who has openly talked about undermining the rule of law. Mr. Trump helped inspire an assault on the Capitol in 2021, has threatened to imprison political adversaries and was denounced as a fascist by former aides. But for his supporters, Mr. Trump’s provocations became selling points rather than pitfalls.
On Wednesday, the results showed Mr. Trump improving on his 2020 showing in a red wave of counties all across America with only limited exceptions. Mr. Trump had flipped Georgia and held North Carolina in the Sun Belt, while sweeping the so-called Blue Wall states of Michigan, Wisconsin and Pennsylvania. The victories vaulted him far past the 270 Electoral College votes he needed to win the White House.
Mr. Trump was leading in the tally of two other swing states — Arizona and Nevada — leaving open the possibility of a clean sweep. He also held an early edge in the popular vote, which he had lost in 2016 even while winning the White House.
Republicans also picked up at least three Senate seats, in Ohio, Montana and West Virginia, to give the party a majority in the Senate. Control of the House of Representatives was still too close to call.
In a victory speech in West Palm Beach, Fla., Mr. Trump declared that he was the leader of “the greatest political movement of all time.”
“We overcame obstacles that nobody thought possible,” he said, adding that he would take office with an “unprecedented and powerful mandate.”
Ms. Harris called Mr. Trump to concede on Wednesday and an aide said they discussed the peaceful transfer of power. She is set to deliver a concession speech at Howard University in Washington in the evening.
Mr. Trump seemingly had to win two races this year.
First, he overcame Mr. Biden, who quit the race after a halting debate performance raised questions about the president’s fitness to serve four more years. Then, he defeated Ms. Harris in a caustic 107-day crucible of a campaign that was ugly, insult-filled and bitter. Mr. Trump questioned Ms. Harris’s racial identity at one point and frequently denigrated her intelligence. They clashed over wildly divergent views of not just the issues facing the country but also the nature of democracy itself.
Mr. Trump has systematically sought to undercut some of the country’s foundational principles, eroding trust in an independent press and the judicial system and sowing doubts about free and fair elections. He has refused to accept his loss four years ago, falsely claiming to this day that a second term was stolen from him in 2020. Instead of hindering his rise, his denial took hold across a Republican Party he remade.
Now, Mr. Trump has vowed a radical reshaping of American government, animated by his promises of “retribution” and of rooting out domestic opponents he casts as “the enemy within.” He has pledged to oversee the biggest wave of deportations in U.S. history, suggested deploying troops domestically, proposed sweeping tariffs and largely advocated the greatest consolidation of power in the history of the American presidency.

An assassination attempt against Mr. Trump happened just days before he took the stage in July at the Republican National Convention in Milwaukee.Credit...Jamie Kelter Davis for The New York Times

Mr. Trump’s campaign had aimed to put together a new political coalition anchored not just by blue-collar white voters but working-class Black and Latino voters, as well. By Wednesday morning, there were some early signs the campaign had succeeded.
The 2024 election is the second time Mr. Trump has defeated a woman trying to break through the nation’s highest gender barrier — the presidency — after he prevailed over Hillary Clinton eight years ago. His history of sexual misconduct, along with his three appointees to the Supreme Court and their role in ending the constitutional right to an abortion in 2022, transformed the race into a referendum on gender and women’s rights.
But abortion may not have been as salient an issue as it was in the 2022 midterm elections. Florida on Tuesday became the first state since Roe v. Wade was overturned to reject an abortion-rights ballot measure.
Polls heading into the election showed a country divided at historic levels along gender lines. Men, including many younger male voters, powered Mr. Trump’s popularity, as women were at the heart of Ms. Harris’s coalition.
It was also the first election in which a major candidate was a felon. Yet the specifics of Mr. Trump’s crimes were rarely broached by Ms. Harris, who instead tried to focus on kitchen-table issues.
In May, in a criminal case brought by the Manhattan district attorney, Mr. Trump was found guilty of 34 felony counts for covering up hush-money payments made to a porn star during the 2016 race. In a sign of the extraordinary circumstances facing him, Mr. Trump awaits sentencing tentatively scheduled for later this month, just as he will be ramping up the presidential transition process.

The race featured more than $1 billion in television advertising alone, as Ms. Harris, 60, offered herself as the vanguard of a new generation of leadership focused on the middle class, rolling out a series of policy plans to tackle grocery prices, housing costs, child care and elder care. She flipped her position on the border, promising a crackdown after arguing when she ran for president in 2019 that it should not be a crime to enter the United States without authorization.
Mr. Trump cast her as responsible for many of the country’s problems, countering with an array of sloganeering tax cuts: no tax on tips, no tax on Social Security, no tax on overtime, among them. He denigrated her as a “stupid person,” and called her “failed” and “dangerously liberal.”
Ms. Harris called for turning the page on the divisive Trump era. “We are not going back,” she said, and crowds chanted the line back. But she could never fully wrest the mantle of change away from Mr. Trump, given her perch as the current president’s second-in-command.
The Biden administration may have accelerated the country’s recovery from the coronavirus pandemic, engineered a softer landing than most economists expected and passed a raft of sweeping legislation tackling manufacturing, climate change and infrastructure. But rising food and housing prices caused a painful economic pinch that packed a political punch.
Mr. Trump also promised to disentangle the country from conflicts abroad, a turn toward isolationism that found a fresh audience with a war raging in Europe between Russia and Ukraine for nearly three years, and with the Middle East on the precipice of a wider conflagration. His election raises questions about the future of NATO and the American backing of Ukraine; Mr. Trump has long spoken glowingly about President Vladimir V. Putin of Russia.
Seeking to blunt the political backlash faced by his party since the Supreme Court overturned Roe, the landmark decision guaranteeing a federal right to an abortion, Mr. Trump adopted a stance of leaving abortion rights to the states.

Ms. Harris outmaneuvered and baited Mr. Trump at their only debate in September.Credit...Hiroko Masuike/The New York Times
Mr. Trump formally declared his candidacy nearly two years ago, just days after the 2022 midterm elections. The reality, though, is that he barely stopped running after losing the 2020 election.
He withstood a ban by social media companies after the violence of Jan. 6, corporate donor boycotts, a $454 million civil fraud judgment against him in New York and multiple indictments, including one for a conspiracy to defraud the United States.
Mr. Trump crushed his Republican rivals into submission. In the 2022 congressional primaries, he unseated eight of the 10 Republican lawmakers who had voted for his second impeachment. Then he swept through the 2024 presidential primaries, winning every state but one after refusing to debate his opponents.
His supporters rallied behind him as a candidate of destiny even before a would-be assassin’s bullet grazed his ear in July, at a rally in Butler, Pa., days before the Republican National Convention. “Fight, fight, fight,” he shouted as he pumped his fist in the air and blood dripped down his face.
Eight days later, Mr. Biden, isolated at his Delaware home after testing positive for Covid, withdrew from the race. Ms. Harris’s entry unleashed a burst of money and momentum. The Democratic Party quickly consolidated behind her as she closed the polling gap with Mr. Trump. In September, she outmaneuvered and baited him at their only debate.
But Mr. Trump’s enduring appeal helped him navigate a bitter final phase that included his former White House chief of staff saying that Mr. Trump met the definition of a “fascist.”
The label did not stick for many voters. Instead, come January, he will again take office as commander in chief.
"""

# Llamada a la función de análisis y mostrar el resultado
resultado = analizar_noticia(texto_ejemplo)
# print(resultado)

def procesar_respuesta(response_text):
    data = {}

    # Sentiment Analysis
    sentiment_regex = r"Positive:\s*(\d\.\d+),\s*Negative:\s*(\d\.\d+),\s*Neutral:\s*(\d\.\d+)"
    sentiment_match = re.search(sentiment_regex, response_text)
    if sentiment_match:
        data["sentiment"] = {
            "positive": float(sentiment_match.group(1)),
            "negative": float(sentiment_match.group(2)),
            "neutral": float(sentiment_match.group(3))
        }

    # Political Bias
    bias_regex = r"Left:\s*(\d\.\d+),\s*Right:\s*(\d\.\d+),\s*Neutral:\s*(\d\.\d+)\.\s*Explanation:\s*(.*)"
    bias_match = re.search(bias_regex, response_text)
    if bias_match:
        data["political_bias"] = {
            "left": float(bias_match.group(1)),
            "right": float(bias_match.group(2)),
            "neutral": float(bias_match.group(3)),
            "explanation": bias_match.group(4).strip()
        }

    # Tone
    tone_regex = r"Tone:\s*(\w+),\s*Intensity:\s*(\d\.\d+)"
    tone_match = re.search(tone_regex, response_text)
    if tone_match:
        data["tone"] = {
            "type": tone_match.group(1),
            "intensity": float(tone_match.group(2))
        }

    # Thematic Classification
    theme_regex = r"Main Category:\s*(\w+),\s*Subtheme:\s*(.*)"
    theme_match = re.search(theme_regex, response_text)
    if theme_match:
        data["thematic_classification"] = {
            "main_category": theme_match.group(1),
            "subtheme": theme_match.group(2).strip()
        }

    # Tags
    tags_regex = r"Tags:\s*(.*)"
    tags_match = re.search(tags_regex, response_text)
    if tags_match:
        data["tags"] = [tag.strip() for tag in tags_match.group(1).split(",")]

    # Locations
    locations_regex = r"Locations:\s*(.*)"
    locations_match = re.search(locations_regex, response_text)
    if locations_match:
        data["locations"] = [location.strip() for location in locations_match.group(1).split(",")]

    # Summary
    summary_regex = r"Summary:\s*(.*)"
    summary_match = re.search(summary_regex, response_text)
    if summary_match:
        data["summary"] = summary_match.group(1).strip()

    # Fact Consistency
    fact_regex = r"Fact Consistency:\s*(.*)"
    fact_match = re.search(fact_regex, response_text)
    if fact_match:
        data["fact_consistency"] = fact_match.group(1).strip()

    # Translations
    translations_regex = {
        "spanish": r"Spanish:\s*\"Title:\s*(.+?),\s*Summary:\s*(.+?)\"",
        "french": r"French:\s*\"Title:\s*(.*?),\s*Summary:\s*(.*?)\"",
        "german": r"German:\s*\"Title:\s*(.*?),\s*Summary:\s*(.*?)\"",
        "portuguese": r"Portuguese:\s*\"Title:\s*(.*?),\s*Summary:\s*(.*?)\"",
        "chinese": r"Chinese:\s*\"Title:\s*(.*?),\s*Summary:\s*(.*?)\"",
    }

    translations = {}
    for language, regex in translations_regex.items():
        match = re.search(regex, response_text)
        if match:
            translations[language] = {
                "title": match.group(1).strip(),
                "summary": match.group(2).strip()
            }
    data["translations"] = translations

    return data

with open("archivo.txt", "w", encoding="utf-8") as archivo:
    archivo.write(resultado)

def insert_article_data(response_data: dict):
    print("Datos recibidos de la API:", response_data)

    try:
        # Conectar a la base de datos
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        # 1. Insertar en la tabla sources (si no existe)
        source_data = response_data['source']
        cursor.execute("""
            INSERT INTO sources (source_name, country, language, political_affiliation, reliability_score, description, founded_year, url)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (source_name) DO NOTHING
            RETURNING source_id
        """, (source_data["name"], source_data.get("country"), source_data.get("language"),
              source_data.get("political_affiliation"), source_data.get("reliability_score"),
              source_data.get("description"), source_data.get("founded_year"), source_data.get("url")))
        
        source_id = cursor.fetchone()
        if source_id is None:
            cursor.execute("SELECT source_id FROM sources WHERE source_name = %s", (source_data["name"],))
            source_id = cursor.fetchone()[0]
        else:
            source_id = source_id[0]

        # 2. Insertar en la tabla articles
        article_data = response_data['article']
        cursor.execute("""
            INSERT INTO articles (source_id, title, content, published_at, url, summary, fact_consistency, language, importance_score)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING article_id
        """, (source_id, article_data["title"], article_data["content"], article_data["published_at"],
              article_data["url"], article_data["summary"], article_data.get("fact_consistency"),
              article_data.get("language"), article_data.get("importance_score")))
        
        article_id = cursor.fetchone()[0]

        # 3. Insertar en la tabla sentiments
        sentiment_data = response_data['sentiment']
        cursor.execute("""
            INSERT INTO sentiments (article_id, positive, negative, neutral)
            VALUES (%s, %s, %s, %s)
        """, (article_id, sentiment_data["positive"], sentiment_data["negative"], sentiment_data["neutral"]))

        # 4. Insertar en la tabla political_bias
        bias_data = response_data['political_bias']
        cursor.execute("""
            INSERT INTO political_bias (article_id, left_bias, right_bias, neutral, explanation)
            VALUES (%s, %s, %s, %s, %s)
        """, (article_id, bias_data["left"], bias_data["right"], bias_data["neutral"], bias_data["explanation"]))

        # 5. Insertar en la tabla tones
        tone_data = response_data['tone']
        cursor.execute("""
            INSERT INTO tones (article_id, tone_type, intensity)
            VALUES (%s, %s, %s)
        """, (article_id, tone_data["type"], tone_data["intensity"]))

        # 6. Insertar en la tabla thematic_classification
        classification_data = response_data['thematic_classification']
        cursor.execute("""
            INSERT INTO thematic_classification (article_id, main_category, subtheme)
            VALUES (%s, %s, %s)
        """, (article_id, classification_data["main_category"], classification_data.get("subtheme")))

        # 7. Insertar en la tabla tags
        tags = response_data['tags']
        for tag in tags:
            cursor.execute("""
                INSERT INTO tags (article_id, tag)
                VALUES (%s, %s)
            """, (article_id, tag))

        # 8. Insertar en la tabla locations
        locations = response_data['locations']
        for location in locations:
            cursor.execute("""
                INSERT INTO locations (article_id, location)
                VALUES (%s, %s)
            """, (article_id, location))

        # 9. Insertar en la tabla translations
        translations = response_data['translations']
        for language, translation in translations.items():
            cursor.execute("""
                INSERT INTO translations (article_id, language, title, summary)
                VALUES (%s, %s, %s, %s)
            """, (article_id, language, translation["title"], translation["summary"]))

        # 10. Insertar en la tabla social_engagement (si existe en los datos de la API)
        if 'social_engagement' in response_data:
            engagement_data = response_data['social_engagement']
            cursor.execute("""
                INSERT INTO social_engagement (article_id, platform, shares, likes, comments, engagement_score)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (article_id, engagement_data["platform"], engagement_data["shares"],
                  engagement_data["likes"], engagement_data["comments"], engagement_data["engagement_score"]))

        # 11. Relación con eventos (si existe en los datos de la API)
        if 'event' in response_data:
            event_data = response_data['event']
            cursor.execute("""
                INSERT INTO events (title, description, event_date, importance_score)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (title) DO NOTHING
                RETURNING event_id
            """, (event_data["title"], event_data.get("description"), event_data.get("event_date"), event_data.get("importance_score")))
            
            event_id = cursor.fetchone()
            if event_id is None:
                cursor.execute("SELECT event_id FROM events WHERE title = %s", (event_data["title"],))
                event_id = cursor.fetchone()[0]
            else:
                event_id = event_id[0]

            # Relacionar el artículo con el evento en article_events
            cursor.execute("""
                INSERT INTO article_events (article_id, event_id)
                VALUES (%s, %s)
            """, (article_id, event_id))

        # Confirmar cambios
        conn.commit()

    except Exception as e:
        print(f"Error al insertar los datos: {e}")
    finally:
        cursor.close()
        conn.close()

res = procesar_respuesta(resultado)
res['source'] = {
        "name": "The New York Times",
        "country": "USA",
        "language": "en",
        "political_affiliation": "left",
        "reliability_score": 0.9,
        "description": "Leading news source in the United States",
        "founded_year": 1851,
        "url": "https://www.nytimes.com"
    }
res['article'] = {
        "title": "Trump Wins 2024 Presidential Election, Defeating Harris",
        "content": "He played on fears of immigrants and economic worries...",
        "published_at": "2024-11-06 08:00:00",
        "url": "https://www.nytimes.com/trump-wins-2024",
        "summary": "Donald J. Trump secures a second term as president...",
        "fact_consistency": "The main claims appear consistent with known facts.",
        "language": "en",
        "importance_score": 0.8
    }
insert_article_data(res)