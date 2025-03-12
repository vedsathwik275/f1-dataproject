
import React, { useState } from 'react';
import { Search, ChevronDown, Check } from 'lucide-react';

interface DataItem {
  id: string;
  name: string;
  code?: string;
  flag?: string;
  year?: number;
}

interface DataBrowserProps {
  title: string;
  items: DataItem[];
  onSelect: (item: DataItem) => void;
  selectedItem?: DataItem;
  type: 'driver' | 'race' | 'year';
}

const DataBrowser: React.FC<DataBrowserProps> = ({
  title,
  items,
  onSelect,
  selectedItem,
  type,
}) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [isOpen, setIsOpen] = useState(false);

  const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchQuery(e.target.value);
  };

  const toggleDropdown = () => {
    setIsOpen(!isOpen);
  };

  const handleSelect = (item: DataItem) => {
    onSelect(item);
    setIsOpen(false);
  };

  const filteredItems = items.filter((item) => {
    const query = searchQuery.toLowerCase();
    return (
      item.name.toLowerCase().includes(query) ||
      (item.code && item.code.toLowerCase().includes(query))
    );
  });

  const renderItem = (item: DataItem) => {
    if (type === 'driver') {
      return (
        <div className="flex items-center">
          {item.flag && (
            <img 
              src={item.flag} 
              alt={`${item.name}'s flag`} 
              className="w-5 h-3 mr-2 object-cover rounded-sm"
            />
          )}
          <span>{item.name}</span>
          {item.code && (
            <span className="ml-2 text-xs bg-f1-dark px-2 py-0.5 rounded text-f1-lightgray">
              {item.code}
            </span>
          )}
        </div>
      );
    }
    
    if (type === 'race') {
      return (
        <div className="flex items-center">
          {item.flag && (
            <img 
              src={item.flag} 
              alt={`${item.name}'s flag`} 
              className="w-5 h-3 mr-2 object-cover rounded-sm"
            />
          )}
          <span>{item.name}</span>
        </div>
      );
    }
    
    if (type === 'year') {
      return <span>{item.name}</span>;
    }

    return <span>{item.name}</span>;
  };

  return (
    <div className="relative">
      <label className="block text-sm font-medium text-f1-silver mb-1">
        {title}
      </label>
      
      <div 
        className="input-field flex items-center justify-between cursor-pointer"
        onClick={toggleDropdown}
      >
        <div className="flex-grow truncate">
          {selectedItem ? (
            renderItem(selectedItem)
          ) : (
            <span className="text-f1-lightgray/50">Select {title.toLowerCase()}...</span>
          )}
        </div>
        <ChevronDown 
          size={16} 
          className={`text-f1-lightgray transition-transform duration-200 ${isOpen ? 'transform rotate-180' : ''}`} 
        />
      </div>
      
      {isOpen && (
        <div className="absolute z-10 mt-1 w-full bg-f1-dark border border-f1-gray/30 rounded-md shadow-lg max-h-60 overflow-auto">
          <div className="sticky top-0 z-20 bg-f1-dark p-2 border-b border-f1-gray/30">
            <div className="relative">
              <Search size={16} className="absolute left-3 top-1/2 transform -translate-y-1/2 text-f1-lightgray" />
              <input
                type="text"
                className="w-full pl-9 pr-3 py-2 bg-f1-charcoal border border-f1-gray/50 rounded-md text-white placeholder-f1-lightgray/50 focus:outline-none focus:ring-1 focus:ring-f1-red/30 text-sm"
                placeholder={`Search ${title.toLowerCase()}...`}
                value={searchQuery}
                onChange={handleSearch}
                onClick={(e) => e.stopPropagation()}
                autoFocus
              />
            </div>
          </div>
          
          <div className="py-1">
            {filteredItems.length > 0 ? (
              filteredItems.map((item) => (
                <div
                  key={item.id}
                  className={`px-4 py-2 hover:bg-f1-gray/20 cursor-pointer flex items-center justify-between ${
                    selectedItem?.id === item.id ? 'bg-f1-gray/20' : ''
                  }`}
                  onClick={() => handleSelect(item)}
                >
                  <div className="flex-grow">{renderItem(item)}</div>
                  {selectedItem?.id === item.id && (
                    <Check size={16} className="text-f1-red" />
                  )}
                </div>
              ))
            ) : (
              <div className="px-4 py-2 text-f1-lightgray/70 text-sm italic">
                No results found
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default DataBrowser;
