# Desktop-Buddy

> Desktop-Buddy 是使用PyQt5开发的一款桌面伙伴程序。

## 目前功能

- `main.py`
  - 换一换（随机更换动图）
  - 换我的图（加载本地动图）
  - 专注（倒计时提醒，目前没有成功！）
  - 退出（退出程序）
- `remove_background.py`
  - 去除`png图`、`jpg图`、`gif图`背景

## 开发环境

- python: 3.11.9

## 运行

1. 克隆本项目

   ```shell
   git clone https://github.com/OnlyAPI/Desktop-Buddy.git
   ```

2. 安装虚拟环境 （可选）

   ```shell
   python -m venv .venv
   ```

3. 激活虚拟环境（可选）

   - windows

     ```shell
     .\.venv\Scripts\activate
     ```

   - mac/linux

     ```shell
     source ./.venv/bin/activate
     ```

4. 安装依赖包

   ```shell
   pip install -r requirements.txt
   ```

5. 启动

   运行 `main.py` 启动桌面伙伴

   运行 `remove_background.py` 自动读取`input`文件夹下的所有文件并去除背景

## 文件夹说明

- `input`: 把需要去除背景的图放在这个文件夹，去除后会将文件备份到`conpleted`文件夹并清空本文件夹
- `output`: `main.py` 文件读取的动图
- `completed`: 备份`input`文件夹中已去除背景的原图

## 注意

> 动图的需要透明背景，可使用`remove_background.py`文件来去除，但是生成效果不是很理想。

## 鸣谢

- 感谢 <https://github.com/Hanzoe/Pet-GPT.git> 仓库的动图资源
