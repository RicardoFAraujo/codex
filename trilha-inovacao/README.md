# Trilha de Inovação CEPUERJ

Site exclusivo da Trilha de Inovação do Centro de Produção da UERJ (CEPUERJ), desenvolvido para engajar colaboradores internos em programas de capacitação em inovação e colaboração.

## 🎨 Design

### Paleta de Cores
- **Azul Principal**: #0072CE - Cor institucional do CEPUERJ
- **Vermelho de Destaque**: #F9423A - Para elementos de ação e destaques
- **Dourado de Destaque**: #AD841F - Para elementos especiais e premiações
- **Cores Complementares**: Branco, cinzas e gradientes sutis

### Tipografia
- **Fonte Principal**: Inter (Google Fonts)
- **Pesos**: 300, 400, 500, 600, 700

## 🚀 Funcionalidades

### Seções Principais
1. **Hero Section**: Apresentação impactante com animações
2. **Workshops**: Cards interativos com informações detalhadas
3. **Estatísticas**: Contadores animados com métricas de impacto
4. **Sobre**: Informações sobre a trilha de inovação
5. **Footer**: Links e informações de contato

### Workshops Destacados
- **Curso Essencial de Inovação e Colaboração**
  - Módulo 1: Dados & Estratégia (16h)
  - Módulo 2: Execução Ágil (20h)
- **Design Thinking Aplicado** (8h)
- **Lean Startup** (12h)
- **Cultura de Inovação** (6h)
- **Colaboração Digital** (10h)

### Recursos Técnicos
- ✅ Design responsivo (mobile-first)
- ✅ Animações CSS e JavaScript
- ✅ Navegação suave (smooth scroll)
- ✅ Efeitos de hover interativos
- ✅ Menu mobile hamburger
- ✅ Carregamento otimizado
- ✅ Acessibilidade (WCAG 2.1)
- ✅ Performance otimizada

## 📱 Responsividade

O site foi desenvolvido com abordagem mobile-first e é totalmente responsivo:
- **Desktop**: Layout em grid com sidebar
- **Tablet**: Adaptação do layout para telas médias
- **Mobile**: Menu hamburger e layout em coluna única

## 🎯 Objetivos

1. **Engajamento**: Interface moderna e atrativa para despertar interesse
2. **Informação**: Apresentação clara dos workshops e seus benefícios
3. **Usabilidade**: Navegação intuitiva e experiência fluida
4. **Conversão**: CTAs efetivos para inscrições nos workshops

## 🛠️ Tecnologias

- **HTML5**: Estrutura semântica
- **CSS3**: Estilização moderna com grid, flexbox e animações
- **JavaScript**: Interatividade e funcionalidades dinâmicas
- **Font Awesome**: Ícones modernos
- **Google Fonts**: Tipografia profissional

## 📦 Estrutura de Arquivos

```
trilha-inovacao/
├── index.html          # Página principal
├── styles.css          # Estilos CSS
├── script.js           # JavaScript interativo
└── README.md           # Documentação
```

## 🚀 Como Usar

1. Abra o arquivo `index.html` em um navegador web moderno
2. O site é estático e não requer servidor
3. Para desenvolvimento local, pode usar um servidor HTTP simples:
   ```bash
   python -m http.server 8000
   # ou
   npx serve .
   ```

## 🎨 Customização

### Cores
As cores principais estão definidas como variáveis CSS no início do arquivo `styles.css`:
```css
:root {
    --primary-blue: #0072CE;
    --accent-red: #F9423A;
    --accent-gold: #AD841F;
    /* ... */
}
```

### Conteúdo
- Workshops podem ser adicionados/editados na seção `#workshops`
- Estatísticas podem ser atualizadas na seção `.stats`
- Informações institucionais na seção `#about`

## 📈 Performance

- **Otimização de imagens**: Logo carregado via CDN oficial
- **CSS minificado**: Estilos organizados e otimizados
- **JavaScript eficiente**: Eventos otimizados e lazy loading
- **Fontes otimizadas**: Carregamento assíncrono do Google Fonts

## ♿ Acessibilidade

- **Navegação por teclado**: Suporte completo
- **Screen readers**: Estrutura semântica adequada
- **Contraste**: Paleta de cores com contraste adequado
- **Focus management**: Estados de foco visíveis
- **Responsive design**: Funciona em todos os dispositivos

## 🔧 Manutenção

### Adicionando Novos Workshops
1. Copie a estrutura de um card existente
2. Atualize as informações específicas
3. Adicione classes CSS se necessário
4. Teste a responsividade

### Atualizando Estatísticas
1. Edite os números na seção `.stats`
2. O JavaScript animará automaticamente os contadores

## 📞 Suporte

Para dúvidas sobre o desenvolvimento ou personalização do site, entre em contato com a equipe de desenvolvimento do CEPUERJ.

---

**Desenvolvido para o CEPUERJ - Centro de Produção da UERJ**
*Transformando ideias em inovação através da capacitação colaborativa*
