function FlyOutMenu(menuId) {
    var self = this,
        wrapper = document.getElementById(menuId),
        menuRoot = this.firstChildByName(wrapper, 'ul');
    this.removeClass(wrapper, 'css-fly-out-menu');
    this.currentItem = null;

    this.setEventListener(document, 'keydown',
        function(event) {
            return self.keydown(event);
        }, false);
    this.setEventListener(menuRoot, 'mouseover',
        function(event) {
            return self.mouseover(event);
        },  true);
    this.setEventListener(menuRoot, 'mouseout',
        function(event) {
            return self.mouseout(event);
        }, true);
    this.setEventListener(menuRoot, 'focus',
        function(event) {
            return self.mouseover(event);
        }, true);
    this.setEventListener(menuRoot, 'blur',
        function(event) {
            return self.mouseout(event);
        }, true);
    this.setEventListener(menuRoot, 'click',
        function(event) {
            return self.click(event);
        }, true);
    this.setUpMenu(menuRoot, 1);
}

FlyOutMenu.prototype.setUpMenu = function(node, depth) {
    var menuItem = null, subMenu = null, previousMenuItem = null,
        menuItems = this.childNodesByName(node, 'li'),
        i = 0;
    node.setAttribute('role', 'role:menu');
    node.firstMenuItem = menuItems[0];
    this.setClass(menuItems[0], 'first-item');
    this.setClass(menuItems[menuItems.length - 1], 'last-item');
    for(i = 0; i < menuItems.length; i++) {
        menuItem = menuItems[i];
        this.setAaaAttribute('level', menuItem, depth);
        menuItem.previousMenuItem = previousMenuItem;
        if(previousMenuItem) {
            previousMenuItem.nextMenuItem = menuItem;
        }
        previousMenuItem = menuItem;
        subMenu = this.firstChildByName(menuItem, 'ul');
        if(subMenu) {
            menuItem.subMenu = subMenu;
            this.setClass(menuItem, 'has-submenu');
            this.setClass(subMenu, 'vertical');
            this.setUpMenu(subMenu, depth + 1);
        } else {
            menuItem.setAttribute('role', 'role:menuitem');
        }
    }
};

FlyOutMenu.prototype.click = function(event) {
    var target = this.getEventTarget(event, 'li'),
        link = this.childNodesByName(target, 'a')[0];
    if(link) {
        document.location = link.href;
    }
};

FlyOutMenu.prototype.mouseover = function(event) {
    var target = this.getEventTarget(event, 'li'),
        pos = 0, width = 0, i = 0,
        parent = target.parentNode.parentNode,
        siblings = this.childNodesByName(target.parentNode, 'li');
    if(this.currentItem) {
        this.blurElement(this.currentItem);
    }
    if(target.timeout) {
        clearTimeout(target.timeout);
    }
    this.setClass(target, 'focused');
    if(target.subMenu && !target.focused) {
    	var self = this;
    	target.timeout = setTimeout(function() {
	        if(self.isClass(target.parentNode, 'horizontal')) {
	        	self.setClass(target, 'open');
	        } else {
	            pos = self.findRealPos(target);
	            width = window.innerWidth ? window.innerWidth : document.body.offsetWidth;
	            if((pos[0] + (target.offsetWidth * 2)) > width) {
	            	self.setClass(target, 'open-left');
	            } else {
	            	self.setClass(target, 'open-right');
	            }
	        }
	        target.subMenu.style.display = "block";
    	}, 75);
    }
    target.focused = true;
    if(parent.focusedChidren) {
        parent.focusedChidren += 1;
    } else {
        parent.focusedChidren = 1;
    }
    for(i = 0; i < siblings.length; i++) {
        if(siblings[i] != target) {
            if(siblings[i].subMenu) {
                this.removeClass(siblings[i], 'open-left');
                this.removeClass(siblings[i], 'open-right');
                this.removeClass(siblings[i], 'open');
                siblings[i].subMenu.style.display = "none";
            }
            this.removeClass(siblings[i], 'focused');
            siblings[i].focused = false;
        }
    }
    if(parent.nodeName.toLowerCase() == 'li') {
        event.newTarget = parent;
        this.mouseover(event);
    }
    this.currentItem = target;
};

FlyOutMenu.prototype.mouseout = function(event) {
    var self = this,
        target = this.getEventTarget(event, 'li'),
        parent = target.parentNode.parentNode;
    self.removeClass(target, 'focused');
    target.focused = false;

    if(target.timeout) {
        clearTimeout(target.timeout);
    }
    target.timeout = setTimeout(function() {
        if(target.subMenu && !target.focused && (!target.focusedChidren || target.focusedChidren < 1)) {
            target.focusedChidren = 0;
            self.removeClass(target, "open-left");
            self.removeClass(target, "open-right");
            self.removeClass(target, "open");
            target.subMenu.style.display = "none";
        }
    }, 500);
    if(parent.nodeName.toLowerCase() == 'li') {
        parent.focusedChidren -= 1;
        event.newTarget = parent;
        this.mouseout(event);
    }
};

FlyOutMenu.prototype.findRealPos = function(obj) {
    var curleft = 0, curtop = 0;
    if(obj.offsetParent) {
        curleft = obj.offsetLeft;
        curtop = obj.offsetTop;
        while (obj = obj.offsetParent) {
            curleft += obj.offsetLeft;
            curtop += obj.offsetTop;
        }
    }
    return [curleft, curtop];
};

FlyOutMenu.prototype.keydown = function(event) {
    // strings declared for better minifaction
    var action = null, actionVector = null, subMenu = null,
        currentItem = this.currentItem,
        next = "next",
        previous = "previous",
        submenu = "sub-menu",
        horizontal = { 39: /*left*/ next, 37: /*right*/ previous,
                 38: /*up*/ previous, 40: /*down*/ submenu
            },
        vertical = { 39: /*left*/ submenu, 37: /*right*/ previous,
                 38: /*up*/ previous, 40: /*down*/ next
            };
    if(currentItem === null) {
        return true;
    } else if(this.isClass(currentItem.parentNode, 'horizontal')) {
        actionVector = horizontal;
    } else {
        actionVector = vertical;
    }
    if(actionVector[event.keyCode] === undefined) {
        return true;
    } else {
        action = actionVector[event.keyCode];
    }

    if(action == next) {
        if(currentItem.nextMenuItem) {
            this.focusElement(currentItem.nextMenuItem);
        }
    } else if(action == subMenu) {
        subMenu = this.firstChildByName(currentItem, 'ul');
        if(subMenu) {
            this.focusElement(subMenu.firstMenuItem);
        }
    } else if(action == previous) {
        if(currentItem.previousMenuItem) {
            this.focusElement(currentItem.previousMenuItem);
        } else if(currentItem.parentNode.parentNode.nodeName.toLowerCase() == 'li') {
            this.focusElement(currentItem.parentNode.parentNode);
        }
    }
    return this.noAction(event);
};

FlyOutMenu.prototype.focusElement = function(node) {
    var link = this.firstChildByName(node, 'a');
    if(link) {
        link.focus();
    } else {
        node.focus();
        this.dispatchEvent(node, "focus");
    }
};

FlyOutMenu.prototype.blurElement = function(node) {
    var link = this.firstChildByName(node, 'a');
    if(link) {
        link.blur();
    } else {
        node.blur();
        this.dispatchEvent(node, "blur");
    }
};

FlyOutMenu.prototype.dispatchEvent = function(node, eventName) {
    var event = document.createEvent("HTMLEvents");
    event.initEvent(eventName, true, true);
    node.dispatchEvent(event);
};

FlyOutMenu.prototype.removeClass = function(node, value) {
    if(node) {
        var currentValue = node.className;
        if(currentValue === null) {
            return;
        }
        node.className = currentValue.replace(new RegExp(value, 'gi'), '').replace(/ +/, ' ');
    }
};

FlyOutMenu.prototype.setClass = function(node, value) {
    if(value !== null) {
        var currentValue = node.className;
        if(currentValue) {
            node.className = currentValue + ' ' + value;
        } else {
            node.className = value;
        }
    }
};

FlyOutMenu.prototype.setEventListener = function(node, event, func, bool) {
    if(node.addEventListener) {
        node.addEventListener(event, func, bool);
    } else {
        node.attachEvent('on'+event, func, bool);
    }
};

FlyOutMenu.prototype.childNodesByName = function(node, name) {
    var result = [],
        childNodes = node.childNodes,
        length = childNodes.length,
        i = 0;
    for(i = 0; i < length; i++) {
        if(childNodes[i].nodeName && childNodes[i].nodeName.toLowerCase() == name.toLowerCase()) {
            result[result.length] = childNodes[i];
        }
    }
    return result;
};

FlyOutMenu.prototype.firstChildByName = function(node, name) {
    var childNodes = node.childNodes,
        length = childNodes.length,
        i = 0;
    for(i = 0; i < length; i++) {
        if(childNodes[i].nodeName.toLowerCase() == name.toLowerCase()) {
            return childNodes[i];
        }
    }
    return null;
};

FlyOutMenu.prototype.setAaaAttribute = function(attribute, node, value) {
    if(node.setAttributeNS) {
        node.setAttributeNS("http://www.w3.org/2005/07/aaa", attribute, value);
    } else {
        node.setAttribute("aaa:" + attribute, value);
    }
    return true;
};

FlyOutMenu.prototype.isClass = function(node, value) {
    if(node.className === null) {
        return false;
    }
    return node.className.match(new RegExp(value, 'gi'));
};

FlyOutMenu.prototype.getTheEventTarget = function(event) {
    if(event.newTarget) { // my own hack
        return event.newTarget;
    } else if(event.target) {
        return event.target;
    } else {
        return event.srcElement;
    }
};

FlyOutMenu.prototype.getEventTarget = function(event, name) {
    var target = this.getTheEventTarget(event);
    if(target !== null && name !== undefined) {
        while(target && target.nodeName.toLowerCase() != name.toLowerCase()) {
            target = target.parentNode;
        }
    }
    return target;
};

FlyOutMenu.prototype.noAction = function(event) {
    if(event.cancelBubble) {
        event.cancelBubble = true;
    } else {
        try {
            event.stopPropagation();
        } catch(e) {}
    }
    return false;
};
