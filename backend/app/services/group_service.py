"""群组服务"""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.group import Group, GroupMember


class GroupService:
    """群组服务"""

    @staticmethod
    def get_groups(db: Session, page: int = 1, page_size: int = 20) -> dict:
        """获取群组列表"""
        from app.utils.pagination import paginate

        query = db.query(Group).filter(Group.is_public == True).order_by(Group.created_at.desc())
        items, total, has_more = paginate(query, page, page_size)

        group_list = []
        for group in items:
            owner = db.query(User).filter(User.id == group.owner_id).first()
            member_count = db.query(GroupMember).filter(GroupMember.group_id == group.id).count()
            group_list.append({
                "id": group.id,
                "name": group.name,
                "description": group.description,
                "owner_id": group.owner_id,
                "owner": {
                    "id": owner.id if owner else None,
                    "nickname": owner.nickname if owner else "已注销",
                    "avatar": owner.avatar if owner else "",
                },
                "is_public": group.is_public,
                "member_count": member_count,
                "created_at": group.created_at.isoformat() if group.created_at else None,
            })

        return {"list": group_list, "total": total, "has_more": has_more}

    @staticmethod
    def create_group(db: Session, user_id: int, name: str, description: str = "", is_public: bool = True) -> Group:
        """创建群组"""
        group = Group(
            name=name,
            description=description,
            owner_id=user_id,
            is_public=is_public,
        )
        db.add(group)
        db.flush()

        # 创建者自动成为管理员
        member = GroupMember(group_id=group.id, user_id=user_id, role="owner")
        db.add(member)
        db.commit()
        db.refresh(group)
        return group

    @staticmethod
    def get_group_detail(db: Session, group_id: int, current_user_id: int = None) -> dict:
        """获取群组详情"""
        group = db.query(Group).filter(Group.id == group_id).first()
        if not group:
            raise HTTPException(status_code=404, detail="群组不存�?)

        owner = db.query(User).filter(User.id == group.owner_id).first()
        members = db.query(GroupMember, User).join(
            User, GroupMember.user_id == User.id
        ).filter(
            GroupMember.group_id == group_id
        ).all()

        is_member = False
        if current_user_id:
            is_member = db.query(GroupMember).filter(
                GroupMember.group_id == group_id,
                GroupMember.user_id == current_user_id
            ).first() is not None

        member_list = []
        for member, user in members:
            member_list.append({
                "id": user.id,
                "nickname": user.nickname,
                "avatar": user.avatar,
                "role": member.role,
            })

        return {
            "id": group.id,
            "name": group.name,
            "description": group.description,
            "owner_id": group.owner_id,
            "owner": {
                "id": owner.id if owner else None,
                "nickname": owner.nickname if owner else "已注销",
                "avatar": owner.avatar if owner else "",
            },
            "is_public": group.is_public,
            "is_member": is_member,
            "members": member_list,
            "member_count": len(member_list),
            "created_at": group.created_at.isoformat() if group.created_at else None,
        }

    @staticmethod
    def join_group(db: Session, group_id: int, user_id: int):
        """加入群组"""
        group = db.query(Group).filter(Group.id == group_id).first()
        if not group:
            raise HTTPException(status_code=404, detail="群组不存�?)

        if not group.is_public:
            raise HTTPException(status_code=403, detail="该群组为私密群组")

        existing = db.query(GroupMember).filter(
            GroupMember.group_id == group_id,
            GroupMember.user_id == user_id
        ).first()

        if existing:
            raise HTTPException(status_code=400, detail="已经是群组成�?)

        member = GroupMember(group_id=group_id, user_id=user_id)
        db.add(member)
        db.commit()

    @staticmethod
    def leave_group(db: Session, group_id: int, user_id: int):
        """退出群�?""
        member = db.query(GroupMember).filter(
            GroupMember.group_id == group_id,
            GroupMember.user_id == user_id
        ).first()

        if not member:
            raise HTTPException(status_code=400, detail="不是群组成员")

        if member.role == "owner":
            raise HTTPException(status_code=400, detail="群主不能退出群组，请先转让群主")

        db.delete(member)
        db.commit()
