from flask import Flask, jsonify, render_template, request, Blueprint
from google.cloud import datastore
import logging
from datetime import date, datetime
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

# Instantiates a client
client = datastore.Client()

class BookmarkTags(UserMixin):
    def __init__(self):
        pass

    def post_bookmark_tags(self, bookmarkid, json):
        checkedTags = json["checkedTags"]
        if checkedTags:
            for checkedtag in checkedTags:
                # 重複チェック
                query = client.query(kind="BookmarkTags")
                query.add_filter('bookmark_id', '=', int(bookmarkid))
                query.add_filter('tag_id', '=', checkedtag)
                result = list(query.fetch())
                if result:
                    continue
                # The Cloud Datastore key for the new entity
                bookmarktag_key = client.key("BookmarkTags")
                # Prepares the new entity
                bookmarktag = datastore.Entity(key=bookmarktag_key)
                bookmarktag["bookmark_id"] = bookmarkid
                bookmarktag["tag_id"] = checkedtag
                bookmarktag["updated_at"] = datetime.utcnow()
                bookmarktag["created_at"] = datetime.utcnow()
                logging.debug(bookmarktag)
                # Saves the entity
                client.put(bookmarktag)


    def show_bookmark_tags(self, bookmarkid):
        logging.debug(bookmarkid)
        kind = "BookmarkTags"
        query = client.query(kind=kind)
        result = list(query.add_filter('bookmark_id', '=', int(bookmarkid)).fetch())
        # 存在チェック
        if not result:
            return ""

        return result

        '''
        bookmark_tags = []
        for item in result:
            tagid = item.tag_id
            key = client.key("Tag", int(tagid))
            tag = client.get(key)
            logging.debug(tag)
            bookmark_tags.append(tag)
        return jsonify(bookmark_tags)
        '''

    def update_bookmark_tags(self, bookmarkid, checkedTags):
        logging.debug(bookmarkid)
        logging.debug(checkedTags)
        #logging.debug(checkedTags[0])
        kind = "BookmarkTags"
        query = client.query(kind=kind)
        result = list(query.add_filter('bookmark_id', '=', int(bookmarkid)).fetch())
        logging.debug(result)
        addlist = []
        deletelist = []
        # 存在チェック
        if not result:
            if checkedTags:
            #if checkedTags[0] is not None:
                for checkedtag in checkedTags:
                    addlist.append(checkedtag)
        else:
            #BookmarkTagsのtag_id文ループ
            for item in result:
                hitflag = False
                if checkedTags:
                #if checkedTags[0] is not None:
                    #BookmarkTags：あり、checkedTags：あり ⇒そのまま
                    for checkedtag in checkedTags:
                        logging.debug(item)
                        logging.debug(item["tag_id"])
                        logging.debug(checkedtag)
                        if item["tag_id"] == checkedtag:
                            logging.debug("そのまま")
                            logging.debug(item["tag_id"])
                            logging.debug(checkedtag)
                            hitflag = True
                        #BookmarkTags：なし、checkedTags：あり ⇒追加
                        #ここで処理はNG
                        else:
                            pass
                            '''
                            logging.debug("追加")
                            logging.debug(checkedtag)
                            addlist.append(checkedtag)
                            '''
                    #BookmarkTags：あり、checkedTags：なし ⇒削除
                    if hitflag == False:
                        logging.debug("削除")
                        logging.debug(item["tag_id"])
                        logging.debug(checkedtag)
                        deletelist.append(item["tag_id"])
                #BookmarkTags：あり、checkedTags：なし ⇒削除
                else:
                    logging.debug("削除")
                    logging.debug(item["tag_id"])
                    logging.debug(checkedtag)
                    deletelist.append(item["tag_id"])

            logging.debug(checkedTags)
            logging.debug(result)
            #checkedTagsのループ
            for checkedtag in checkedTags:
                for item in result:
                    logging.debug(item)
                    #BookmarkTags：あり、checkedTags：あり ⇒そのまま
                    if item["tag_id"] == checkedtag:
                        pass
                    #BookmarkTags：なし、checkedTags：あり ⇒追加
                    else:
                        logging.debug("追加")
                        logging.debug(checkedtag)
                        addlist.append(checkedtag)

        if deletelist:
            #削除
            for tagid in deletelist:
                query = client.query(kind=kind)
                query.add_filter('bookmark_id', '=', int(bookmarkid))
                query.add_filter('tag_id', '=', tagid)
                result = list(query.fetch())
                for item in result:
                    logging.debug(item)
                    client.delete(item)

        if addlist:
            #追加
            for tagid in addlist:
                # 重複チェック
                query = client.query(kind=kind)
                query.add_filter('bookmark_id', '=', int(bookmarkid))
                query.add_filter('tag_id', '=', tagid)
                result = list(query.fetch())
                if result:
                    continue

                # The Cloud Datastore key for the new entity
                bookmarktag_key = client.key(kind)
                # Prepares the new entity
                bookmarktag = datastore.Entity(key=bookmarktag_key)
                bookmarktag["bookmark_id"] = int(bookmarkid)
                bookmarktag["tag_id"] = tagid
                bookmarktag["updated_at"] = datetime.utcnow()
                bookmarktag["created_at"] = datetime.utcnow()
                logging.debug(bookmarktag)
                # Saves the entity
                client.put(bookmarktag)

        query = client.query(kind=kind)
        query.add_filter('bookmark_id', '=', int(bookmarkid))
        result = list(query.fetch())
        return result

    def get_bookmark_tags(self):
        logging.debug('now in get bookmark_tags')
        kind = "BookmarkTags"
        query = client.query(kind=kind)
        result = list(query.fetch())
        if not result:
            logging.debug('now leave get bookmark_tags')
            return ""
        logging.debug('now leave get bookmark_tags')
        return result
        # return jsonify(result)

    def delete_bookmarks(self, targetid):
        logging.debug('now in delete bookmarks in bookmark_tags')
        # The kind for the new entity
        kind = "BookmarkTags"
        query = client.query(kind=kind)
        query.add_filter('bookmark_id', '=', int(targetid))
        result = list(query.fetch())
        logging.debug(result)
        if result:
            for item in result:
                logging.debug(item)
                client.delete(item)
        logging.debug('now leave delete bookmarks in bookmark_tags')

    def delete_tags(self, targetid):
        logging.debug('now in delete tags in bookmark_tags')
        # The kind for the new entity
        kind = "BookmarkTags"
        query = client.query(kind=kind)
        query.add_filter('tag_id', '=', int(targetid))
        result = list(query.fetch())
        logging.debug(result)
        if result:
            for item in result:
                logging.debug(item)
                client.delete(item)
        logging.debug('now leave delete tags in bookmark_tags')
