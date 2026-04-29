# Textbook Domain Service 仕様まとめ

Textbook削除は論理削除とする。

Textbook.delete()でis_public = Falseにする
TextbookMetadata.delete()でdeleted_atを設定する
title、author_ids、chapter_idsは変更しない
通常取得ではdeleted_at is NoneのTextbookのみ返す
公開取得ではさらにis_public is TrueのTextbookのみ返す
Chapter削除はChapter自体に削除状態を持たせない。

Chapter.delete()は作らない
タイトル・本文のマスクもしない
親Textbook.chapter_idsから対象chapter_idを外す
Textbook単位で取得する前提なので、配列から外れれば表示されない
Domain Service 構成

CreateTextbookDomainService

Textbook.new()でTextbookを作成する
TextbookMetadata.new()でMetadataを作成する
CreateTextbookOutput(textbook, metadata)を返す
DeleteTextbookDomainService

Textbook.delete()を呼ぶ
TextbookMetadata.delete()を呼ぶ
戻り値はなし
ModifyTextbookDomainService

Textbook集約の変更ルールをまとめるDomain Service。

Textbook本体の編集
例: title
必要ならis_public
Chapter追加
Chapter.new()でChapterを作成
Textbook.chapter_idsへ追加
作成したChapterを返す
Chapter削除
Chapter自体は変更しない
Textbook.chapter_idsから対象IDを外す
変更があった場合のみTextbookMetadata.update()
1クラスにメソッドを生やす方針でOK
ModifyChapterDomainService

Chapter Entity自体の編集を担当する。

Chapter.title変更
Chapter.content変更
変更があった場合のみTextbookMetadata.update()
設計方針

Domain Serviceを細かくクラス分割しすぎない
ModifyTextbookDomainServiceはTextbook集約の変更ルールをまとめる
ユースケース単位の細かい分割はApplication層で扱う
ModfiyはtypoなのでModifyにする
metadata更新は「実際に変更があった場合のみ」がAccount側と一貫する