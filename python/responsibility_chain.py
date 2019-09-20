#coding=utf-8
#
# 责任链模式
#

class AbstractContactsProcessor(object):
    """
    contacts 合并链 抽象类
    """
    def __init__(self, child):
        self.child = child
        self.fallthrough = False

    def merge_contacts(self, contacts, **kwargs):
        """
        :param contacts:
        :param kwargs:
        :return:
        """
        raise NotImplementedError

    def process(self, contacts, **kwargs):
        """
        处理入口
        :param contacts:
        :param kwargs:
        :return:
        """
        cs = self.merge_contacts(contacts, **kwargs)

        if self.child and self.fallthrough:
            return self.child.process(cs, **kwargs)
        return cs


class NoahContactsProcessor(AbstractContactsProcessor):
    def merge_contacts(self, contacts, **kwargs):
	contacts.append('noah')
        self.fallthrough = True
        return contacts


class MergeProcessor(AbstractContactsProcessor):
    def merge_contacts(self, contacts, **kwargs):
	contacts.append('merge')
        self.fallthrough = True
        return contacts


class ContainerProcessor(AbstractContactsProcessor):
    def merge_contacts(self, contacts, **kwargs):
	contacts.append('container')
	return contacts


class InfraProcessor(AbstractContactsProcessor):
    def merge_contacts(self, contacts, **kwargs):
	contacts.append('infra')
        return contacts


class NoContactsProcessor(AbstractContactsProcessor):
    def merge_contacts(self, contacts, **kwargs):
	contacts.append('noah')
        return contacts


class DefaultProcessor(AbstractContactsProcessor):
    def merge_contacts(self, contacts, **kwargs):
	contacts.append('default')
        return contacts


class ContactsMerge(object):
    def __init__(self):
        # 定义合并链, 注意顺序
        default = DefaultProcessor(None)
        no_contacts = NoContactsProcessor(default)
        infra = InfraProcessor(no_contacts)
        container = ContainerProcessor(infra)
        merge = MergeProcessor(container)
        noah = NoahContactsProcessor(merge)

        self.processor = noah

    def merge(self, contacts, **kwargs):
        return self.processor.process(contacts, **kwargs)


if __name__ == '__main__':
    cm = ContactsMerge()
    contacts = cm.merge([])
    print(contacts)

