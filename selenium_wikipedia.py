import time
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ExtratorWikiJSON:
    """
    Classe para automação da extração de dados da Wikipedia.
    Combina Selenium (interação) e BeautifulSoup (extração).
    """
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.vars = {}

    def teardown(self):
        """Fecha o navegador e encerra a sessão do driver."""
        self.driver.quit()

    def executar_extracao(self):
        url = "https://pt.wikipedia.org/wiki/Python"
        print(f"🔄 Acessando: {url}")
        self.driver.get(url)
        self.driver.set_window_size(1200, 900)

        wait = WebDriverWait(self.driver, 10)
        titulo_elemento = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#firstHeading")))
        
        print("⌨️  Executando ActionChains (Clique + Setas do Teclado)...")
        actions = ActionChains(self.driver)
        actions.click(titulo_elemento) \
               .send_keys(Keys.ARROW_DOWN) \
               .send_keys(Keys.ARROW_DOWN) \
               .pause(1) \
               .perform() 
        
        print("📄 Capturando o HTML da página...")
        conteudo_html = self.driver.page_source
        soup = BeautifulSoup(conteudo_html, 'html.parser')

        titulo_texto = soup.find(id="firstHeading").get_text()
        
        conteudo_div = soup.find(id="bodyContent")
        paragrafos = conteudo_div.find_all('p')
        lista_resumo = []
        for p in paragrafos:
            texto = p.get_text().strip()
            if texto:
                lista_resumo.append(texto)
            if len(lista_resumo) >= 3:
                break

        dados_finais = {
            "titulo": titulo_texto,
            "url_origem": url,
            "resumo": lista_resumo,
            "metadados": {
                "capturado_em": time.strftime("%Y-%m-%d %H:%M:%S"),
                "tecnologia": "Selenium + BeautifulSoup"
            }
        }

        nome_arquivo = "resumo_python.json"
        with open(nome_arquivo, "w", encoding="utf-8") as json_file:
            json.dump(dados_finais, json_file, indent=4, ensure_ascii=False)
        
        print(f"✅ Sucesso! Dados salvos em '{nome_arquivo}'")
        print("\n--- Prévia do JSON ---")
        print(json.dumps(dados_finais, indent=4, ensure_ascii=False))
        print("----------------------\n")

if __name__ == "__main__":
    bot = ExtratorWikiJSON()
    try:
        bot.executar_extracao()
        
        input("🛑 O navegador está aberto. Pressione [ENTER] neste terminal para fechar e encerrar...")
        
    except Exception as e:
        print(f"❌ Erro durante a execução: {e}")
    finally:
        print("👋 Encerrando o driver...")
        bot.teardown()