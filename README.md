
# FirefighterProblemSimulation

## 介紹
該模擬器能實際沙盤推演救火決策，同步展示該決策導致之火勢發展變化，並能與整數規劃模型或啟發式演算法所得解法的救火決策比較，透過這種視覺化的模擬訓練方式，
可讓消防決策人員能藉由練習與觀察以學習收斂其指揮與調度救火人員與資源的成效。


## 功能
該模擬器提供五個主要功能，包括問題介紹、教學、案例模式、隨機網路模式以及解法播放器，以下為

**1. 問題介紹**：以簡潔的文字引導使用者快速理解本研究之問題背景和設定。

**2. 教學**：透過提示視窗教學，幫助使用者逐步熟悉模擬器的介面和操作方式。

**3. 案例模式**：轉換現實案例至本研究之問題設定，以更具現實性的案例呈現本
研究問題的真實性並進行案例模擬。我們以 2021 玉山森林大火事件作為現實
案例，將森林、露營地以及村落地區作為網路圖的節點，森林步道和連接村
落與露營地的道路則構成網路圖的節線。

**4. 隨機網路模式**：讀取系統內部檔案生成對應的網路圖以及各種參數如消防員
的移動速度、火焰的傳播速度以及節點容量等，進行隨機網路模擬。

**5. 解法播放器**：載入由整數規劃模型以及本研究之啟發式演算法生成結果之 json
檔案，以視覺化方式重新推演救火過程。

## 安裝教學
**1.create your own git repository**

git clone https://github.com/pinanlee/FirefighterProblemSimulation.git 

**2. open cmd**

cd "YOUR_GIT_REPOSITORY"\FirefighterProblemSimulation

python Start.py

## 研究來源

考慮燃料管理的移動消防員問題最佳化研究：整數規劃、啟發式演算法與視覺化模擬器之設計與應用

Optimization of the Moving Firefighter Problem considering Fuel Management: Integer Programming, Meta-heuristics, 
and a Visualized Simulator

指導教授 王逸琳 教授

孫秉新 劉耀文 彭真人 詹詠吏 李品安

https://drive.google.com/file/d/1TBM18dwhkN18wj518LKnRLWW77jskH30/view?usp=drive_link
