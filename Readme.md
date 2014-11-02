MHA-VPC
=========================
MySQL Master HA(MHA)をAWS-VPC環境で動作させた時に、
Routing-VIPを新masterに向け直すスクリプト

使い方
------
    /etc/mha.cnf

    [server default]
    master_ip_failover_script=/root/mha-vpc/Mha-vpc.py
    report_script=/root/mha-vpc/Report.py

前提条件
------
1. rootユーザーで各MySQLインスタンスがパス無し鍵認証接続できること
2. MHA(manager / node)がMySQLインスタンスにインストールされていること
3. 各MySQLインスタンスのENIについて、Source/Desc CheckがOFFになっていること
4. 各MySQLインスタンスが所属するRoutingテーブルにvipを設定し、Master-MySQLのENIにDestinationを向けること
5. boto / paramiko がインストールされていること

設定ファイル
------
- config/aws_key.json : AWSアクセスキー, AWSシークレットキー, リージョンを指定
- config/route_table.json : VPCのRoutingテーブルのid, vip, Routingテーブル名
- Report.py : レポートメールの送信元/送信先メールアドレス


フェイルオーバーの流れ
------
1. MHAがmaster死亡を検知
2. MHAによって以下がキックされる(stopssh)
`/root/mha-vpc/Mha-vpc.py --orig_master_host=旧masterホスト名 --orig_master_ip=旧masterIP --orig_master_port=旧masterport --command=stopssh --ssh_user=SSH接続ユーザ名`
3. 2によってRoutingテーブルから旧masterIPが削除、旧masterインスタンスをシャットダウン
4. MHAが新masterを選出、レプリケーション再構築
5. MHAによって以下がキックされる(start)
`/root/mha-vpc/Mha-vpc.py --command=start --ssh_user=ssh接続ユーザ名 --new_master_host=新masterホスト名 --new_master_ip=新masterIP --new_master_port=新masterのport `
6. 5によって、新masterをRoutingテーブルに登録
7. Report.pyがキックされて、フェイルオーバー完了をメールで通知

参照
------
<https://code.google.com/p/mysql-master-ha/>
<http://d.hatena.ne.jp/c9katayama/20111225/1324837509>
