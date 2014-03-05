/*
 * Script from www.ueue.cc [by Harveyqing]
 * @requires jQuery($), jQuery UI & sortable/draggable UI modules
 */

var iNettuts = {
    
    jQuery : $,
    
    settings : {
        columns : '.editor-pic-ul',              // 外部ul
        widgetSelector: '.progressWrapper',      // class为widget的元素是将需要被拖动的元素
        handleSelector: '.editor-pic-move',
        contentSelector: '.widget-content',
        widgetDefault : {                        // 可拖动框框的默认属性
            movable: true,                       // 可移动
            removable: true,                     // 可删除
        }
    },
    // 初始化
    init : function () {
        this.addWidgetControls();                   // 加载对“可拖动框框”的控制--删除、编辑、折叠
        this.makeSortable();
    },
    
    // 获取widget的设置
    getWidgetSettings : function (id) {     // 这里的id是待拖动元素的id
        var $ = this.jQuery,
            settings = this.settings;
        // 如果id不为false，则设置为widgetIndividual；否则返回默认设置项
        return settings.widgetDefault;
    },
    
    addWidgetControls : function () {
        var iNettuts = this,
            $ = this.jQuery,
            settings = this.settings;
        var movableItems = $(settings.widgetSelector, $(settings.columns));

        $.each(movableItems, function () {
            var thisWidgetSettings = settings.widgetDefault; // iNettuts.getWidgetSettings(this.id);   // 获取该id元素的设置项
            if (thisWidgetSettings.removable) {     // 可删除
                $('.editor-pic-del').mousedown(function (e) {  // 按下可拖动元素右上角'x'时，下面的this指向x元素
                    e.stopPropagation();    // 将该事件（mousedown只限于本对象上不影响DOM和父元素）的默认事件响应清除    
                }).click(function () {
                        $(this).parents(settings.widgetSelector).animate({  // 选中承载这个x的框框
                            opacity: 0
                        },function () {     // 下面的this指向可拖动的框框元素
                            // console.log($(this));
                            $(this).wrap('<div/>').parent().slideUp(function () {   // 先将这个框框用<div></div>包裹起来，parent即指整个div，然后向上滑动
                                $(this).remove();   // 将整个div从DOM中删掉
                            });
                        });
                    return false;   // 阻止所选元素click的默认行为，详见http://stackoverflow.com/questions/11184276/return-false-from-jquery-click-event
                });  // 如果可删除，将其添加至可移动框框的头部;这里的this指向each的每个元素
            }
        });
        
    },
    
    makeSortable : function () {
        
        var iNettuts = this,    // 这里的this指向整个iNettuts对象
            $ = this.jQuery,    
            settings = this.settings,

            $sortableItems = (function () {
                var notSortable = '';
                $(settings.widgetSelector,$(settings.columns)).each(function (i) {  // 这里的i是匹配的元素位置索引
                    if (!iNettuts.getWidgetSettings(this.id).movable) { // this指匹配的元素 ； 如果不可以移动
                        if(!this.id) {  // 该元素没有id
                            this.id = 'widget-no-id-' + i;
                        }
                        notSortable += '#' + this.id + ',';
                    }
                });
                var tempSelector = '> li:not('+notSortable+')';
                return $('> li', settings.columns);    // 选择出可以移动的li
            })();
        $sortableItems.find(settings.handleSelector).css({  
            cursor: 'move'      // 将find出来的特定（可移动）框框的头部cursor设为
        }).mousedown(function (e) {
            $sortableItems.css({width:''});     // 这里的作用是？ （
            $(this).parent().css({  // 这里的this是指框框的头部
                width: $(this).parent().width() + 'px'  // 给li添加width属性，这里给定一个固定的宽度，使得待拖动的框框能定宽，否则拖动时被撑到100%宽
            });
        }).mouseup(function () {
            if(!$(this).parent().hasClass('dragging')) {    // 待拖动框框没有dragging属性
                $(this).parent().css({width: $(this).parent().width() + 'px'});
            } else {
                $(settings.columns).sortable('disable');
            }
        });

        $(settings.columns).sortable({
            items: $sortableItems,                  // 制定在settings.columns选择的元素里哪些元素是可排序的
            connectWith: $(settings.columns),
            handle: settings.handleSelector,
            // placeholder: 'widget-placeholder',
            // forcePlaceholderSize: true,
            revert: 300,
            delay: 100,
            opacity: 0.7,
            containment: 'document',
            start: function (e,ui) {
                $(ui.helper).addClass('dragging');
            },
            stop: function (e,ui) {
                $(ui.item).css({width:''}).removeClass('dragging');
                $(settings.columns).sortable('enable');
            }
        });
    }
  
};

iNettuts.init();