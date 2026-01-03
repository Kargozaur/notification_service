"""initial data for notification channel

Revision ID: feda8d3c24ee
Revises: 1ff3928b66e9
Create Date: 2026-01-03 20:36:53.406864

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "feda8d3c24ee"
down_revision: Union[str, Sequence[str], None] = "1ff3928b66e9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("""
        INSERT INTO notification_channels (type, display_name, requires_auth, default_settings, is_active)
        VALUES
            ('email',       'Email',            false, '{}', true),
            ('telegram',    'Telegram',         true,  '{}', true),
            ('web-push',    'Web Push',         true,  '{}', true),
            ('sms',         'SMS',              true,  '{}', false),
            ('discord',     'Discord Webhook',  true,  '{}', false),
            ('slack',       'Slack',            true,  '{}', false),
            ('whatsapp',    'WhatsApp',         true,  '{}', false)
        ON CONFLICT (type) DO NOTHING;
    """)


def downgrade():
    op.execute("""
        DELETE FROM notification_channels 
        WHERE type IN (
            'email', 'telegram', 'web-push', 'sms', 
            'discord', 'slack', 'whatsapp'
        );
    """)
