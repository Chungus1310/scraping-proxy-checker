# 🌐 Proxy Scraper & Checker

A robust Python tool that scrapes proxy servers from multiple sources and validates them against specified websites. Perfect for maintaining an up-to-date list of working proxies for your web scraping needs!

## ✨ Features

- Scrapes proxies from 15+ different sources
- Validates proxy format and functionality
- Multi-threaded proxy checking
- Intelligent retry mechanism with backoff strategy
- Random User-Agent rotation
- Comprehensive logging
- Saves both raw and working proxies to separate files

## 🚀 Getting Started

### Prerequisites

Make sure you have Python 3.6+ installed on your system. You'll also need the following packages:

```bash
pip install requests beautifulsoup4 fake-useragent urllib3
```

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Chungus1310/scraping-proxy-checker.git
cd scraping-proxy-checker
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## 🔧 Usage

Simply run the script:

```bash
python get.py
```

The script will:
1. Fetch proxies from multiple sources
2. Save all unique proxies to `proxy.txt`
3. Test each proxy against specified websites
4. Save working proxies to `working_proxies.txt`

## 📝 Configuration

The script comes with sensible defaults, but you can modify these settings in the code:

- `test_urls`: URLs used to validate proxies (default: Yandex services)
- `max_workers`: Number of concurrent threads for proxy checking (default: 4000)
- `timeout`: Connection timeout in seconds (default: 10)
- `retry_strategy`: Number of retries and backoff factor for failed requests

## 🔍 How It Works

1. **Proxy Collection**: The script fetches proxy lists from various sources including:
   - GitHub repositories
   - Public proxy APIs
   - Free proxy websites

2. **Validation Process**:
   - Checks proxy format validity
   - Verifies proxy connectivity
   - Tests proxy functionality with target websites
   - Uses random delays to avoid rate limiting

3. **Output**:
   - Detailed logging of the entire process
   - Two output files: all proxies and working proxies

## ⚠️ Important Notes

- Some proxy sources might be unavailable at times
- Free proxies can be unreliable and should not be used for sensitive tasks
- Consider rate limiting when testing against websites
- Use responsibly and in accordance with target websites' terms of service

## 🤝 Contributing

Contributions are welcome! Feel free to:

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the Apache License - see the LICENSE file for details.

## 💡 Acknowledgments

- Thanks to all the proxy list providers
- Inspired by various proxy checking tools in the community
- Built with love for the web scraping community

## 📞 Contact

Got questions or suggestions? Open an issue on GitHub!

Happy scraping! 🎉
