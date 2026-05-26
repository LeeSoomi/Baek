<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>비밀번호 경우의 수 계산기</title>
  <style>
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: Arial, sans-serif;
      background: #f3f5f7;
      color: #222;
    }
    .app {
      width: 100%;
      max-width: 430px;
      min-height: 100vh;
      margin: 0 auto;
      background: white;
      padding: 28px 22px;
    }
    .screen { display: none; }
    .screen.active { display: block; }
    h1 {
      text-align: center;
      font-size: 24px;
      margin: 20px 0 80px;
      padding: 18px;
      border: 2px solid #222;
      border-radius: 25px;
    }
    h2 {
      text-align: center;
      font-size: 22px;
      margin: 20px 0 35px;
      padding: 15px;
      border: 2px solid #222;
      border-radius: 20px;
    }
    .main-btn, .back-btn {
      width: 100%;
      padding: 18px;
      margin: 22px 0;
      border: 2px solid #222;
      border-radius: 18px;
      background: white;
      font-size: 21px;
      cursor: pointer;
    }
    .main-btn:hover, .back-btn:hover { background: #eef2ff; }
    label {
      display: block;
      margin-top: 18px;
      font-weight: bold;
      font-size: 16px;
    }
    input, select {
      width: 100%;
      padding: 13px;
      margin-top: 8px;
      border: 2px solid #aaa;
      border-radius: 10px;
      font-size: 16px;
    }
    .result-box {
      margin-top: 24px;
      padding: 18px;
      border: 2px solid #222;
      border-radius: 15px;
      background: #fafafa;
      line-height: 1.7;
      font-size: 16px;
      word-break: break-all;
    }
    .small-text {
      color: #555;
      font-size: 13px;
      margin-top: 6px;
    }
  </style>
</head>
<body>
  <div class="app">
    <!-- 1번 화면 -->
    <section id="home" class="screen active">
      <h1>비밀번호 경우의 수 계산기</h1>
      <button class="main-btn" onclick="showScreen('caseScreen')">경우의 수 계산</button>
      <button class="main-btn" onclick="showScreen('hackScreen')">해킹 시간 계산</button>
    </section>

    <!-- 2번 화면 -->
    <section id="caseScreen" class="screen">
      <h2>경우의 수 계산</h2>

      <label>비밀번호 길이</label>
      <input type="number" id="pwLength" min="1" value="8" oninput="calculateCases()" />
      <div class="small-text">직접 입력하세요.</div>

      <label>문자 종류</label>
      <select id="charType" onchange="calculateCases()">
        <option value="10">숫자만</option>
        <option value="52">영어만</option>
        <option value="62">영어 + 숫자</option>
        <option value="94">영어 + 숫자 + 특수문자</option>
      </select>

      <label>반복 사용 가능 여부</label>
      <select id="repeatType" onchange="calculateCases()">
        <option value="yes">반복 가능</option>
        <option value="no">반복 불가능</option>
      </select>

      <div class="result-box">
        <b>경우의 수</b>
        <div id="caseResult">-</div>
        <br />
        <b>추천 비밀번호</b>
        <div id="recommendPw">-</div>
      </div>

      <button class="back-btn" onclick="showScreen('home')">이전</button>
    </section>

    <!-- 4번 화면 -->
    <section id="hackScreen" class="screen">
      <h2>해킹 시간 계산</h2>

      <label>나의 비밀번호</label>
      <input type="text" id="myPw" placeholder="비밀번호 입력" oninput="calculateHackTime()" />
      <div class="small-text">1초에 100,000,000가지 시도한다고 가정합니다.</div>

      <label>해킹 시간</label>
      <div class="result-box" id="hackTime">-</div>

      <label>보안등급</label>
      <div class="result-box" id="securityLevel">-</div>

      <button class="back-btn" onclick="showScreen('home')">이전</button>
    </section>
  </div>

  <script>
    function showScreen(screenId) {
      document.querySelectorAll('.screen').forEach(screen => screen.classList.remove('active'));
      document.getElementById(screenId).classList.add('active');
    }

    function formatBigNumber(num) {
      return num.toLocaleString('ko-KR') + '가지';
    }

    function permutation(n, r) {
      if (r > n) return 0;
      let result = 1;
      for (let i = 0; i < r; i++) result *= (n - i);
      return result;
    }

    function makePassword(length, type) {
      // 비밀번호 길이, 문자 종류, 반복 가능 여부를 먼저 확인한 뒤 추천 비밀번호 생성
      const lower = 'abcdefghijklmnopqrstuvwxyz';
      const upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
      const numbers = '0123456789';
      const symbols = '!@#$%^&*?';

      const repeat = document.getElementById('repeatType').value;

      let chars = '';
      if (type == 10) chars = numbers;
      else if (type == 52) chars = lower + upper;
      else if (type == 62) chars = lower + upper + numbers;
      else chars = lower + upper + numbers + symbols;

      if (repeat === 'no' && length > chars.length) {
        return '조건에 맞는 비밀번호를 만들 수 없음';
      }

      let password = '';

      // 중복 없는지 확인하는 함수
      function hasNoDuplicate(text) {
        return new Set(text.split('')).size === text.length;
      }

      // 조건에 맞는 문자인지 확인하는 함수
      function fitsType(text) {
        for (let ch of text) {
          if (!chars.includes(ch)) return false;
        }
        return true;
      }

      // 문자 추가 함수: 반복 불가능이면 이미 쓴 문자는 제외
      function addRandomChar(source) {
        let possible = source.split('').filter(ch => repeat === 'yes' || !password.includes(ch));
        if (possible.length === 0) return;
        password += possible[Math.floor(Math.random() * possible.length)];
      }

      // 반복 가능: robotA7!처럼 단어 활용
      if (repeat === 'yes') {
        const easyWords = ['robot', 'river', 'tiger', 'apple', 'dream', 'light', 'music', 'green'];

        if (type != 10 && length >= 6) {
          const word = easyWords[Math.floor(Math.random() * easyWords.length)];
          password += word.slice(0, Math.min(word.length, Math.floor(length / 2)));
        }
      }

      // 반복 불가능: sky, run, cat처럼 중복 없는 짧은 단어 조각 활용
      else {
        const shortWords = ['sky', 'run', 'cat', 'blue', 'star', 'wolf', 'bird', 'fish', 'rock', 'wind'];
        const usableWords = shortWords.filter(word => hasNoDuplicate(word) && fitsType(word) && word.length <= length);

        if (type != 10 && usableWords.length > 0 && length >= 3) {
          const word = usableWords[Math.floor(Math.random() * usableWords.length)];
          password += word;
        }
      }

      // 문자 종류별로 보안성을 높이기 위해 필요한 문자를 우선 추가
      if (type == 62 || type == 94) addRandomChar(numbers);
      if (type == 52 || type == 62 || type == 94) addRandomChar(upper);
      if (type == 94) addRandomChar(symbols);

      // 남은 길이 채우기
      while (password.length < length) {
        addRandomChar(chars);
      }

      password = password.slice(0, length);
      return password;
    }

    function capitalize(word) {
      return word.charAt(0).toUpperCase() + word.slice(1);
    }

    function calculateCases() {
      const length = Number(document.getElementById('pwLength').value);
      const charCount = Number(document.getElementById('charType').value);
      const repeat = document.getElementById('repeatType').value;

      if (!length || length < 1) {
        document.getElementById('caseResult').textContent = '-';
        document.getElementById('recommendPw').textContent = '-';
        return;
      }

      let cases;
      if (repeat === 'yes') cases = Math.pow(charCount, length);
      else cases = permutation(charCount, length);

      document.getElementById('caseResult').textContent = formatBigNumber(cases);
      document.getElementById('recommendPw').textContent = makePassword(length, charCount);
    }

    function getCharSetSize(password) {
      let size = 0;
      if (/[0-9]/.test(password)) size += 10;
      if (/[a-z]/.test(password)) size += 26;
      if (/[A-Z]/.test(password)) size += 26;
      if (/[^0-9a-zA-Z]/.test(password)) size += 32;
      return size;
    }

    function formatTime(seconds) {
      if (seconds < 60) return seconds.toFixed(2) + '초';
      const minutes = seconds / 60;
      if (minutes < 60) return minutes.toFixed(2) + '분';
      const hours = minutes / 60;
      if (hours < 24) return hours.toFixed(2) + '시간';
      const days = hours / 24;
      if (days < 365) return days.toFixed(2) + '일';
      const years = days / 365;
      return years.toExponential(2) + '년';
    }

    function calculateHackTime() {
      const pw = document.getElementById('myPw').value;
      if (pw.length === 0) {
        document.getElementById('hackTime').textContent = '-';
        document.getElementById('securityLevel').textContent = '-';
        return;
      }

      const charSet = getCharSetSize(pw);
      const cases = Math.pow(charSet, pw.length);
      const seconds = cases / 100000000;

      document.getElementById('hackTime').textContent = formatTime(seconds);

      let level = '';
      if (seconds < 60) level = '낮음';
      else if (seconds < 86400) level = '보통';
      else if (seconds < 31536000) level = '높음';
      else level = '매우 높음';

      document.getElementById('securityLevel').textContent = level;
    }

    calculateCases();
  </script>
</body>
</html>
