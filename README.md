# uncomment

<div align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-blue.svg" alt="Version 1.0.0">
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License MIT">
  <img src="https://img.shields.io/badge/python-3.6+-yellow.svg" alt="Python 3.6+">
  <img src="https://img.shields.io/badge/flask-2.3.3-red.svg" alt="Flask 2.3.3">
</div>

<p align="center">
  <img src="https://raw.githubusercontent.com/viktorexe/uncomment/main/static/img/logo.png" alt="uncomment Logo" width="200">
</p>

> A modern, intelligent code comment removal tool supporting 20+ programming languages

## ✨ Features

- **Multi-Language Support**: Handles 20+ programming languages with specialized comment handling
- **Smart Detection**: Preserves string literals while removing comments
- **Modern UI**: Dark/light theme with syntax highlighting and line numbers
- **Code Analysis**: Get insights about your code before processing
- **Instant Processing**: Remove comments with a single click
- **Download or API**: Get results as downloadable files or via JSON API

## 🚀 Demo

Try it live at [uncomment.vercel.app](https://uncomment.vercel.app)

![Uncomment Demo](https://raw.githubusercontent.com/viktorexe/uncomment/main/static/img/demo.gif)

## 🔧 Supported Languages

| Language | Single-line | Multi-line |
|----------|-------------|------------|
| Python | `#` | `"""..."""` or `'''...'''` |
| JavaScript | `//` | `/*...*/` |
| TypeScript | `//` | `/*...*/` |
| Java | `//` | `/*...*/` |
| C/C++ | `//` | `/*...*/` |
| C# | `//` | `/*...*/` |
| HTML | - | `<!--...-->` |
| CSS | - | `/*...*/` |
| SCSS/LESS | `//` | `/*...*/` |
| Ruby | `#` | `=begin...=end` |
| Kotlin | `//` | `/*...*/` |
| Swift | `//` | `/*...*/` |
| Dart | `//` | `/*...*/` |
| Go | `//` | `/*...*/` |
| Rust | `//` | `/*...*/` |
| PHP | `//` | `/*...*/` |
| SQL | `--` | `/*...*/` |
| PowerShell | `#` | `<#...#>` |
| YAML | `#` | - |

## 🛠️ Installation

### Prerequisites
- Python 3.6+
- Flask

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/viktorexe/uncomment.git
   cd uncomment
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python app.py
   ```

4. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

## 📚 API Usage

### Remove Comments

```bash
curl -X POST http://localhost:5000/remove_comments \
  -F "code=function hello() { // This is a comment\n  console.log('Hello'); }" \
  -F "language=javascript" \
  -F "format=json"
```

Response:
```json
{
  "original_size": 58,
  "processed_code": "function hello() { \n  console.log('Hello'); }",
  "processed_size": 41,
  "reduction_percentage": "29.3%"
}
```

### Analyze Code

```bash
curl -X POST http://localhost:5000/api/analyze \
  -F "code=function hello() { // This is a comment\n  console.log('Hello'); }" \
  -F "language=javascript"
```

Response:
```json
{
  "code_hash": "a1b2c3d4e5f6g7h8i9j0",
  "comment_lines": 1,
  "estimated_reduction": "25.0%",
  "language": "javascript",
  "total_lines": 2
}
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

- [Flask](https://flask.palletsprojects.com/) - The web framework used
- [Prism.js](https://prismjs.com/) - For syntax highlighting
- [Vercel](https://vercel.com/) - For hosting the application

---

<div align="center">
  Made with ❤️ by <a href="https://github.com/viktorexe">viktorexe</a>
</div>