from notion_client import Client

# 👇 Your Notion integration token
notion = Client(auth="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")

# 👇 Your database ID
DATABASE_ID = "22edd85a-f722-8009-b77f-c72b5fa611d6"

def push_to_notion(resume, score, reason):
    try:
        notion.pages.create(
            parent={"database_id": DATABASE_ID},
            properties={
                "Resume": {
                    "title": [
                        {
                            "text": {"content": resume}
                        }
                    ]
                },
                "Score": {
                    "number": score
                },
                "Reason": {
                    "rich_text": [
                        {
                            "text": {"content": reason}
                        }
                    ]
                }
            }
        )
        print(f"✅ Sent to Notion: {resume}, {score}")
    except Exception as e:
        print("❌ Notion error:", e)
