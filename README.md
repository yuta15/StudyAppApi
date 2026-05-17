# StudyApp API

## ローカル開発

初回は環境変数ファイルを用意し、依存関係を同期する。

```bash
cp .env.example .env
uv sync
```

ローカル用コンテナを起動し、migration を適用してから API を起動する。

```bash
make container-up
make migration-upgrade
make dev
```

必要に応じて開発用 seed data を投入できる。

```bash
make db-seed-dev
```

## Makefile

よく使うコマンドは以下。

| コマンド | 内容 |
| --- | --- |
| `make container-up` | PostgreSQL と Firebase Emulator を起動 |
| `make container-down` | ローカル用コンテナを停止 |
| `make db-ps` | DB コンテナの状態を確認 |
| `make db-shell` | DB コンテナへ入る |
| `make db-psql` | DB に `psql` 接続 |
| `make db-seed-dev` | 開発用 seed data を投入 |
| `make migration-upgrade` | 最新 migration を適用 |
| `make migration-downgrade` | migration を 1 つ戻す |
| `make unit-test` | unit test を実行 |
| `make integration-test` | integration test を実行 |
| `make dev` | 開発サーバーを起動 |

## Firebase Emulator を使った開発

`make container-up` で Firebase Auth Emulator も一緒に起動する。  
ローカル開発では `.env.example` の値をベースに、以下の設定を使う。

```env
FIREBASE_AUTH_EMULATOR_HOST=localhost:9099
FIREBASE_PROJECT_ID=study-local
```

起動後は以下を利用できる。

- Auth Emulator: `localhost:9099`
- Emulator UI: `http://localhost:4000`

API は `FIREBASE_AUTH_EMULATOR_HOST` が設定されている環境で起動すると、ローカルの Firebase Auth Emulator を利用して認証を検証する。
